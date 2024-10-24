from fastapi import APIRouter, HTTPException
from app.services.github import fetch_repo, fetch_repo_json
from app.services.gpt import analyze_code
from loguru import logger

router = APIRouter()

@router.post("/review")
async def review_code(assignment_description: str = "thats mvp of the project, that have to load all files in github repo and analyze it",
                      github_repo_url: str = "https://github.com/rykovlad/CodeReviewAITestTask.git",
                      candidate_level: str = "Junior"):
    try:
        repo_content = await fetch_repo(github_repo_url)

        review = await analyze_code(assignment_description, repo_content, candidate_level)

        return {"result": review}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
