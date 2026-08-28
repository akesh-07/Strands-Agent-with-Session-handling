from datetime import datetime
from strands.tools import tool
from app.core.logging import logger

MANDATORY_DOCUMENTS = [
    "Refund application form",
    "Written request for cancellation/withdrawal",
    "Admission confirmation letter",
    "Fee payment receipt",
    "Student identity card",
    "Bank account details with cancelled cheque/passbook copy"
]

@tool
def check_refund_documents_and_eligibility(withdrawal_date: str, last_date_of_admission: str, documents_ready: list[str]) -> str:
    """
    Check the refund percentage eligibility based on the withdrawal date and last date of admission,
    and verify if all mandatory documents are present.
    
    Args:
        withdrawal_date (str): The date the student withdrew, in YYYY-MM-DD format.
        last_date_of_admission (str): The formally notified last date of admission, in YYYY-MM-DD format.
        documents_ready (list[str]): A list of documents the student says they have ready.
        
    Returns:
        str: A formatted string summarizing the refund eligibility percentage and listing any missing mandatory documents.
    """
    logger.info(f"Running check_refund_documents_and_eligibility for withdrawal_date: {withdrawal_date}, last_date_of_admission: {last_date_of_admission}")
    
    try:
        w_date = datetime.strptime(withdrawal_date, "%Y-%m-%d")
        a_date = datetime.strptime(last_date_of_admission, "%Y-%m-%d")
    except ValueError:
        return "Error: Dates must be provided in YYYY-MM-DD format."
        
    # Calculate difference in days
    delta_days = (w_date - a_date).days
    
    # Determine percentage based on matrix
    if delta_days <= -15:
        percentage = "100%"
    elif -15 < delta_days < 0:
        percentage = "90%"
    elif 0 <= delta_days <= 15:
        percentage = "80%"
    elif 15 < delta_days <= 30:
        percentage = "50%"
    else:
        percentage = "0%"
        
    # Check documents
    # Using lowercase for simple loose matching
    ready_docs_lower = [doc.lower() for doc in documents_ready]
    missing_docs = []
    
    for req_doc in MANDATORY_DOCUMENTS:
        is_present = False
        req_doc_lower = req_doc.lower()
        
        for ready_doc in ready_docs_lower:
            # Check if any significant word matches to be lenient
            if ready_doc in req_doc_lower or req_doc_lower in ready_doc:
                is_present = True
                break
                
        if not is_present:
            missing_docs.append(req_doc)
            
    # Format the result
    result = f"Refund Eligibility: The withdrawal is {abs(delta_days)} days {'before' if delta_days < 0 else 'after'} the last date of admission. The student is eligible for a {percentage} refund of the academic fee."
    
    if missing_docs:
        result += "\n\nMissing Mandatory Documents: The student still needs to submit:\n"
        for doc in missing_docs:
            result += f"- {doc}\n"
    else:
        result += "\n\nAll mandatory documents appear to be ready."
        
    return result
