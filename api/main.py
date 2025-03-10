# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.proposal_service import get_proposal

app = FastAPI(title="AI Pre-Sales Proposal Generator API", version="1.0")

class ProposalRequest(BaseModel):
    input_text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Pre-Sales Proposal Generator API!"}

@app.post("/generate_proposal")
def generate_proposal_endpoint(request: ProposalRequest):
    """
    API endpoint to generate a project proposal.
    Accepts project requirements and returns the proposal JSON along with a formatted document.
    """
    try:
        result = get_proposal(request.input_text, formatted=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
