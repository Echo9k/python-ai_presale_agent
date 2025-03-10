# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.proposal_service import get_proposal
from utils.logger import logger


app = FastAPI(title="AI Pre-Sales Proposal Generator API", version="1.0")

class ProposalRequest(BaseModel):
    input_text: str
    include_context: bool = False

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Pre-Sales Proposal Generator API!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate_proposal")
def generate_proposal_endpoint(request: ProposalRequest):
    logger.info("Received proposal generation request")
    try:
        result = get_proposal(request.input_text, formatted=True, include_context=request.include_context)
        logger.info("Proposal generated successfully")
        return result
    except Exception as e:
        logger.error(f"Error generating proposal: {e}")
        raise HTTPException(status_code=500, detail=str(e))
