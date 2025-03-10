# tests/test_proposal.py
from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Pre-Sales Proposal Generator API!"}

def test_generate_proposal():
    payload = {
        "input_text": "We are launching a new AI solution for retail analytics. The project should analyze market trends, define cost-effective strategies, estimate project duration, and detail necessary team roles along with key assumptions and warranty terms."
    }
    response = client.post("/generate_proposal", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Check that the keys exist in the response
    assert "json" in data
    assert "document" in data
    # Optionally, validate that each section is populated
    for key in ["cost_estimation", "duration_estimation", "team_composition", "assumptions", "warranty_details"]:
        assert key in data["json"]
        assert isinstance(data["json"][key], str)
