import json
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
from strands.tools import tool
from app.core.config import settings
from app.core.logging import logger

@tool
def log_anonymous_anti_ragging_complaint(incident_description: str, location: str, offender_details: str = "Not provided") -> str:
    """
    Log an anonymous anti-ragging complaint directly to the administration's secure database (S3).
    Use this tool when a user reports being a victim of or witnessing ragging, bullying, or harassment.
    
    Args:
        incident_description (str): A detailed description of what happened.
        location (str): Where the incident occurred (e.g., "Hostel B", "Cyber/Online", "Classroom 101").
        offender_details (str, optional): Any known details about the offenders. Defaults to "Not provided".
        
    Returns:
        str: A confirmation message containing a unique tracking ticket ID.
    """
    logger.info("Running log_anonymous_anti_ragging_complaint tool.")
    
    if not settings.S3_BUCKET:
        logger.error("S3_BUCKET is not configured. Cannot log complaint.")
        return "Error: Internal system configuration error. Please contact administration directly."
        
    ticket_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    complaint_data = {
        "ticket_id": ticket_id,
        "timestamp": timestamp,
        "incident_description": incident_description,
        "location": location,
        "offender_details": offender_details
    }
    
    try:
        s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
        object_key = f"anti-ragging-complaints/{ticket_id}.json"
        
        s3_client.put_object(
            Bucket=settings.S3_BUCKET,
            Key=object_key,
            Body=json.dumps(complaint_data, indent=2),
            ContentType="application/json"
        )
        
        logger.info(f"Successfully logged anonymous complaint. Ticket ID: {ticket_id}")
        
        return (
            f"The complaint has been successfully and anonymously logged to the Anti-Ragging Committee. "
            f"Your secure tracking ticket ID is {ticket_id}. "
            f"Please save this ID if you need to follow up with the administration."
        )
        
    except ClientError as e:
        logger.error(f"Failed to upload complaint to S3: {e}")
        return "Error: Failed to securely log the complaint due to a server error. Please try again or contact the nodal officer directly."
