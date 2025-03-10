# services/proposal_service.py
from chains.proposal_chain import generate_proposal, assemble_proposal_document, assemble_proposal_markdown
from utils.context_loader import load_context_documents
from utils.logger import logger

def get_proposal(input_text: str, formatted: bool = True, include_context: bool = False, 
                 industry: str = "general", tone: str = "professional", output_format: str = "plain") -> dict:
    """
    Orchestrates the proposal generation process.
    """
    logger.debug("Starting proposal service with parameters: input_text=%s, include_context=%s, industry=%s, tone=%s, output_format=%s",
                 input_text, include_context, industry, tone, output_format)
    
    if include_context:
        logger.debug("Loading context documents...")
        context = load_context_documents()
        input_text = context + "\n\n" + input_text
        logger.debug("Context appended to input text.")

    try:
        proposal_json = generate_proposal(input_text, industry=industry, tone=tone)
    except Exception as e:
        logger.error("Error generating proposal JSON in service", exc_info=True)
        raise e

    result = {"json": proposal_json}
    if formatted:
        try:
            if output_format.lower() == "markdown":
                proposal_doc = assemble_proposal_markdown(proposal_json)
            else:
                proposal_doc = assemble_proposal_document(proposal_json)
            result["document"] = proposal_doc
            logger.debug("Formatted document generated.")
        except Exception as e:
            logger.error("Error formatting proposal document", exc_info=True)
            raise e

    logger.debug("Proposal service completed successfully with result: %s", result)
    return result
