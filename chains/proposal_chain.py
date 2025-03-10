# chains/proposal_chain.py
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.config import settings
from utils.logger import logger

logger.debug("Initializing Groq LLM...")

# Initialize Groq LLM using config values
llm = ChatGroq(
    model_name=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE,
    api_key=settings.GROQ_API_KEY
)

logger.debug("Groq LLM initialized with model: %s", settings.MODEL_NAME)

# Define the expected JSON structure for the proposal output
proposal_structure = {
    "type": "object",
    "properties": {
        "cost_estimation": {"type": "string"},
        "duration_estimation": {"type": "string"},
        "team_composition": {"type": "string"},
        "assumptions": {"type": "string"},
        "warranty_details": {"type": "string"}
    },
    "required": [
        "cost_estimation",
        "duration_estimation",
        "team_composition",
        "assumptions",
        "warranty_details"
    ]
}

logger.debug("Setting up JSON parser with structure: %s", proposal_structure)

# Initialize the JSON output parser with the defined structure
parser = JsonOutputParser(pydantic_object=proposal_structure)

# Create a prompt template that includes placeholders for industry and tone.
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are an AI assistant that generates project proposals for AI consulting projects in the {industry} industry. "
            "The proposal should adopt a {tone} tone. Based on the input provided, please produce a proposal in JSON format with the following structure:\n\n"
            "{{\n"
            '  "cost_estimation": "Estimated cost details here",\n'
            '  "duration_estimation": "Estimated duration details here",\n'
            '  "team_composition": "Details of required team here",\n'
            '  "assumptions": "Key assumptions listed here",\n'
            '  "warranty_details": "Warranty and support information here"\n'
            "}}\n\n"
            "Ensure that all fields are populated with a concise yet informative description."
        )
    ),
    ("user", "{input}")
])

logger.debug("Prompt template created.")

# Chain the prompt, LLM, and parser
chain = prompt | llm | parser

def generate_proposal(input_text: str, industry: str = "general", tone: str = "professional") -> dict:
    """
    Generates a project proposal based on the input text, industry, and tone.
    """
    logger.debug("Generating proposal with input: %s, industry: %s, tone: %s", input_text, industry, tone)
    try:
        result = chain.invoke({"input": input_text, "industry": industry, "tone": tone})
        logger.debug("Proposal generated: %s", result)
        return result
    except Exception as e:
        logger.error("Error generating proposal", exc_info=True)
        raise e

def assemble_proposal_document(proposal: dict) -> str:
    """
    Formats the JSON proposal into a human-readable plain text document.
    """
    logger.debug("Assembling plain text document from proposal: %s", proposal)
    try:
        document = (
            "=== Project Proposal ===\n\n"
            "1. Cost Estimation\n"
            "-------------------\n"
            f"{proposal.get('cost_estimation', 'N/A')}\n\n"
            "2. Duration Estimation\n"
            "-----------------------\n"
            f"{proposal.get('duration_estimation', 'N/A')}\n\n"
            "3. Team Composition\n"
            "--------------------\n"
            f"{proposal.get('team_composition', 'N/A')}\n\n"
            "4. Assumptions\n"
            "--------------\n"
            f"{proposal.get('assumptions', 'N/A')}\n\n"
            "5. Warranty Details\n"
            "-------------------\n"
            f"{proposal.get('warranty_details', 'N/A')}\n"
        )
        logger.debug("Plain text document assembled.")
        return document
    except Exception as e:
        logger.error("Error assembling plain text document", exc_info=True)
        raise e

def assemble_proposal_markdown(proposal: dict) -> str:
    """
    Formats the JSON proposal into a Markdown formatted document.
    """
    logger.debug("Assembling Markdown document from proposal: %s", proposal)
    try:
        markdown_doc = (
            "# Project Proposal\n\n"
            "## Cost Estimation\n"
            f"{proposal.get('cost_estimation', 'N/A')}\n\n"
            "## Duration Estimation\n"
            f"{proposal.get('duration_estimation', 'N/A')}\n\n"
            "## Team Composition\n"
            f"{proposal.get('team_composition', 'N/A')}\n\n"
            "## Assumptions\n"
            f"{proposal.get('assumptions', 'N/A')}\n\n"
            "## Warranty Details\n"
            f"{proposal.get('warranty_details', 'N/A')}\n"
        )
        logger.debug("Markdown document assembled.")
        return markdown_doc
    except Exception as e:
        logger.error("Error assembling Markdown document", exc_info=True)
        raise e
