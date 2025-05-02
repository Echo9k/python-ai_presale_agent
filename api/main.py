# api/main.py
from sanic import Sanic, Request
from sanic.response import json, file as sanic_file # Renamed to avoid conflict
from sanic.exceptions import SanicException, NotFound, ServerError
from sanic_ext import Extend, validate
from api.documents import bp as documents_bp

from pydantic import BaseModel
from services.proposal_service import get_proposal
from utils.logger import logger
import os # To potentially get PORT for Cloud Run

# Define the request model (remains the same)
class ProposalRequest(BaseModel):
    input_text: str
    include_context: bool = False
    industry: str = "general"
    tone: str = "professional"
    output_format: str = "markdown"  # Options: "plain" or "markdown"

app = Sanic("AIPreSalesProposalGeneratorAPI")
Extend(app)
app.blueprint(documents_bp)

# --- Routes ---

# Serve the front-end index.html when visiting the root URL
@app.get("/")
async def read_root(request: Request):
    logger.debug("Serving index.html from frontend directory")
    try:
        # Construct the full path relative to the script's location might be safer
        # Assuming 'frontend' is at the same level as 'api'
        base_dir = os.path.dirname(os.path.dirname(__file__)) # Go up one level from api/
        file_path = os.path.join(base_dir, "frontend", "index.html")
        return await sanic_file(file_path)
    except FileNotFoundError:
        logger.error("index.html not found.")
        raise NotFound("index.html not found")

# Health check endpoint
@app.get("/health")
async def health_check(request: Request):
    logger.debug("Health check endpoint accessed.")
    return json({"status": "ok"})

# API endpoint to generate a proposal
@app.post("/generate_proposal")
@validate(json=ProposalRequest) # Use sanic-ext to validate Pydantic model
async def generate_proposal_endpoint(request: Request, body: ProposalRequest): # Validated body is passed
    logger.info("Received proposal generation request: %s", body)
    try:
        result = get_proposal(
            body.input_text,
            formatted=True, # Assuming this should always be true for the API
            include_context=body.include_context,
            industry=body.industry,
            tone=body.tone,
            output_format=body.output_format
        )
        logger.info("Proposal generated successfully.")
        return json(result) # Return JSON response
    except Exception as e:
        logger.error("Error generating proposal in API endpoint", exc_info=True)
        # Raise a Sanic exception for internal server errors
        raise ServerError(f"Internal server error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, dev=True)
