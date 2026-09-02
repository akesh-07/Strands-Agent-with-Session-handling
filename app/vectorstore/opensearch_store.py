import boto3
from typing import List
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from app.core.config import settings
from app.core.logging import logger
from app.models.document import Chunk

class OpenSearchStore:
    def __init__(self):
        """Initializes the OpenSearch client with AWS SigV4 auth."""
        self.host = settings.OPENSEARCH_HOST
        if self.host and self.host.startswith('https://'):
            self.host = self.host.replace('https://', '')
            
        self.index_name = settings.OPENSEARCH_INDEX_NAME
        self.region = settings.AWS_REGION

        # Setup AWS Auth for OpenSearch Serverless (service name: aoss)
        credentials = boto3.Session().get_credentials()
        
        if not credentials:
            logger.warning("No AWS credentials found. OpenSearch auth will fail.")
            self.awsauth = None
        else:
            self.awsauth = AWS4Auth(
                credentials.access_key,
                credentials.secret_key,
                self.region,
                'aoss',
                session_token=credentials.token
            )
        
        if not self.host:
            logger.warning("OpenSearch host is not set. OpenSearchStore will fail if invoked.")
            self.client = None
            return

        self.client = OpenSearch(
            hosts=[{'host': self.host, 'port': 443}],
            http_auth=self.awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=30
        )

    def _create_index_if_missing(self, dimension: int):
        """Creates a k-NN index in OpenSearch Serverless if it does not exist."""
        if not self.client:
            return
            
        if not self.client.indices.exists(index=self.index_name):
            logger.info(f"Creating OpenSearch vector index '{self.index_name}' with dimension {dimension}")
            body = {
                "settings": {
                    "index": {
                        "knn": True
                    }
                },
                "mappings": {
                    "properties": {
                        "embedding": {
                            "type": "knn_vector",
                            "dimension": dimension,
                            "method": {
                                "name": "hnsw",
                                "space_type": "l2"
                            }
                        },
                        "text": { "type": "text" },
                        "filename": { "type": "keyword" },
                        "page_number": { "type": "integer" }
                    }
                }
            }
            self.client.indices.create(index=self.index_name, body=body)
            # AOSS requires sleeping a bit for the index to be ready for indexing
            import time
            time.sleep(2)

    def save_index(self):
        """No-op for OpenSearch as documents are indexed immediately over HTTP."""
        pass

    def add_vectors(self, vectors: List[List[float]], chunks: List[Chunk]):
        """Bulk indexes embeddings and text chunks into OpenSearch."""
        if not self.client or not vectors:
            return

        dimension = len(vectors[0])
        self._create_index_if_missing(dimension)
        
        logger.info(f"Indexing {len(vectors)} chunks into OpenSearch...")
        bulk_body = []
        for i, (vector, chunk) in enumerate(zip(vectors, chunks)):
            bulk_body.append({
                "index": {
                    "_index": self.index_name,
                    "_id": f"{chunk.metadata.filename}_{chunk.metadata.page_number}_{i}"
                }
            })
            bulk_body.append({
                "embedding": vector,
                "text": chunk.text,
                "filename": chunk.metadata.filename,
                "page_number": chunk.metadata.page_number,
                "chunk_id": chunk.metadata.chunk_id
            })
            
        # Execute bulk request
        response = self.client.bulk(body=bulk_body)
        if response.get('errors'):
            logger.error("Errors occurred during OpenSearch bulk indexing.")
        else:
            logger.info("Successfully indexed vectors to OpenSearch.")

    def similarity_search(self, query_vector: List[float], top_k: int = None) -> List[Chunk]:
        """Performs a k-NN similarity search against OpenSearch."""
        if not self.client:
            return []
            
        if top_k is None:
            top_k = settings.TOP_K

        body = {
            "size": top_k,
            "query": {
                "knn": {
                    "embedding": {
                        "vector": query_vector,
                        "k": top_k
                    }
                }
            },
            "_source": ["text", "filename", "page_number", "chunk_id"]
        }

        try:
            res = self.client.search(index=self.index_name, body=body)
            hits = res["hits"]["hits"]
            
            results = []
            for hit in hits:
                source = hit["_source"]
                # Reconstruct the Chunk model to match FAISS output
                from app.models.document import ChunkMetadata
                metadata = ChunkMetadata(
                    filename=source.get("filename", "unknown"),
                    page_number=source.get("page_number", 1),
                    chunk_id=source.get("chunk_id", hit.get("_id", "unknown"))
                )
                chunk = Chunk(
                    text=source.get("text", ""),
                    metadata=metadata
                )
                results.append(chunk)
                
            return results
        except Exception as e:
            logger.error(f"OpenSearch search failed: {e}")
            return []
