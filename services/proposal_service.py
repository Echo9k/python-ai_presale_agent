# services/proposal_service.py
from chains.proposal_chain import generate_proposal, assemble_proposal_document
from utils.context_loader import load_context_documents
from utils.logger import logger


def get_proposal(input_text: str, formatted: bool = True, include_context: bool = False) -> dict:
    """
    Orchestrates the proposal generation process.

    Args:
        input_text (str): Project description.
        formatted (bool): Whether to return a formatted document.
        include_context (bool): Whether to load and include context documents in the input.

    Returns:
        dict: Contains the raw JSON proposal and optionally a formatted document.
    """
    if include_context:
        context = load_context_documents()
        # Append the context to the input text
        input_text = context + "\n\n" + input_text

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
