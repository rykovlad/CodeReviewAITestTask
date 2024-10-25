from fastapi import APIRouter, HTTPException
from loguru import logger

from app.models.review import ReviewRequest
from app.services.github import fetch_repo
from app.services.gpt import analyze_code

router = APIRouter()

@router.post("/review")
async def review_code(review_request: ReviewRequest):
    """
    assignment_description: a brief description of the project
    github_repo_url: str, that have owner and repo_name in it
    candidate_level: Junior, Middle or Senior only
    """
    try:
        repo_content = await fetch_repo(review_request.github_repo_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem with github parsing\n" + str(e))

    try:
        review = await analyze_code(review_request.assignment_description, repo_content, review_request.candidate_level)
        return {"result": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem with openAI\n" + str(e))
