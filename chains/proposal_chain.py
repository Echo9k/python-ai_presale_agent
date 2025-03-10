# chains/proposal_chain.py
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from utils.config import settings


# Initialize Groq LLM using config values
llm = ChatGroq(
    model_name=settings.MODEL_NAME,
    temperature=settings.TEMPERATURE,
    api_key=settings.GROQ_API_KEY
)

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

# Initialize the JSON output parser with the defined structure
parser = JsonOutputParser(pydantic_object=proposal_structure)

# Create a prompt template for generating the proposal.
# Use double curly braces to escape the JSON structure.
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        (
            "You are an AI assistant that generates project proposals for AI consulting projects. "
            "Based on the input provided, please produce a proposal in JSON format with the following structure:\n\n"
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

# Chain the prompt, LLM, and parser together
chain = prompt | llm | parser

def generate_proposal(input_text: str) -> dict:
    """
    Generates a project proposal based on the input text.

    Args:
        input_text (str): A description containing project requirements and context.

    Returns:
        dict: The proposal details in JSON format.
    """
    result = chain.invoke({"input": input_text})
    return result


def assemble_proposal_document(proposal: dict) -> str:
    """
    Formats the JSON proposal into a Markdown-formatted document.

    Args:
        proposal (dict): Proposal details in JSON format.

    Returns:
        str: A Markdown-formatted proposal document.
    """
    markdown_document = (
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
    return markdown_document
