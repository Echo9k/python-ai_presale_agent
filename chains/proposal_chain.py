import os
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Initialize Groq LLM with the model and temperature
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=groq_api_key
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
# Notice the use of double curly braces to escape the JSON structure
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

# Chain the prompt, LLM, and parser to ensure JSON output
chain = prompt | llm | parser

def generate_proposal(input_text: str) -> dict:
    """
    Generates a project proposal based on the input text.

    Args:
        input_text (str): A description containing project requirements and context.

    Returns:
        dict: A dictionary with the proposal details including cost, duration, team, assumptions, and warranty.
    """
    result = chain.invoke({"input": input_text})
    return result

if __name__ == "__main__":
    # Example project description to generate a proposal
    input_description = (
        "We are launching a new AI solution for retail analytics. The project should analyze current market trends, "
        "determine cost-effective strategies, estimate project duration, and define necessary team roles. "
        "It must also list key assumptions and include warranty and support terms."
    )
    
    proposal = generate_proposal(input_description)
    print("Generated Proposal:")
    print(json.dumps(proposal, indent=2))