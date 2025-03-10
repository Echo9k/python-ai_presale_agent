# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.proposal_service import get_proposal
from utils.logger import logger


app = FastAPI(title="AI Pre-Sales Proposal Generator API", version="1.0")

# Serve the front-end index.html when visiting the root URL
@app.get("/")
def read_root():
    logger.debug("Serving index.html from frontend directory")
    return FileResponse("frontend/index.html")

# Health check endpoint
@app.get("/health")
def health_check():
    logger.debug("Health check endpoint accessed.")
    return {"status": "ok"}

# Define the request model for proposal generation
class ProposalRequest(BaseModel):
    input_text: str
    include_context: bool = False
    industry: str = "general"
    tone: str = "professional"
    output_format: str = "markdown"  # Options: "plain" or "markdown"

# API endpoint to generate a proposal
@app.post("/generate_proposal")
def generate_proposal_endpoint(request: ProposalRequest):
    logger.info("Received proposal generation request: %s", request)
    try:
        result = get_proposal(
            request.input_text,
            formatted=True,
            include_context=request.include_context,
            industry=request.industry,
            tone=request.tone,
            output_format=request.output_format
        )
        logger.info("Proposal generated successfully.")
        return result
    except Exception as e:
        logger.error("Error generating proposal in API endpoint", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
