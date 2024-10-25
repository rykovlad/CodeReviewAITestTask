import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.review import ReviewRequest

client = TestClient(app)

@pytest.fixture
def mock_review_request():
    return ReviewRequest(
        assignment_description="The project should load code from GitHub and analyze it with ChatGPT by certain criteria.",
        github_repo_url="https://github.com/rykovlad/CodeReviewAITestTask",
        candidate_level="Junior"
    )

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "i`m alive\n go to http://localhost:8000/docs"}

def test_review_code(mock_review_request):
    response = client.post("/api/v1/review", json=mock_review_request.dict())
    assert response.status_code == 200
    res = response.json()
    assert "analyzed_files" in res
    assert "issues" in res
    assert "rating" in res
    assert "conclusion" in res

    assert isinstance(res["analyzed_files"], list), "here is a meaningful description of the error, but I don't have tiiiiiiiiime"
    assert isinstance(res["rating"], str)
    assert isinstance(res["conclusion"], str)

    assert isinstance(res["issues"], list)
    assert isinstance(res["issues"][0], dict)

    issue_exemple = res["issues"][0]
    assert "file" in issue_exemple
    assert "description" in issue_exemple

    assert isinstance(issue_exemple["description"], list)
    assert isinstance(issue_exemple["description"][0], str)

