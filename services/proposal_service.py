# services/proposal_service.py
from chains.proposal_chain import generate_proposal, assemble_proposal_document

def get_proposal(input_text: str, formatted: bool = True) -> dict:
    """
    Orchestrates the proposal generation process.

    Args:
        input_text (str): Project description.
        formatted (bool): Whether to return a formatted document alongside raw JSON.

    Returns:
        dict: Contains the raw JSON proposal and optionally a formatted document.
    """
    proposal_json = generate_proposal(input_text)
    if formatted:
        proposal_doc = assemble_proposal_document(proposal_json)
        return {
            "json": proposal_json,
            "document": proposal_doc
        }
    return {"json": proposal_json}
