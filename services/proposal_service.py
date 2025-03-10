# services/proposal_service.py
from chains.proposal_chain import generate_proposal, assemble_proposal_document
from utils.logger import logger

def get_proposal(input_text: str, formatted: bool = True) -> dict:
    """
    Orchestrates the proposal generation process.
    """
    try:
        proposal_json = generate_proposal(input_text)
    except Exception as e:
        logger.error("Error in generating proposal JSON", exc_info=True)
        raise e

    if formatted:
        try:
            proposal_doc = assemble_proposal_document(proposal_json)
        except Exception as e:
            logger.error("Error in assembling proposal document", exc_info=True)
            raise e

        return {
            "json": proposal_json,
            "document": proposal_doc
        }
    return {"json": proposal_json}
