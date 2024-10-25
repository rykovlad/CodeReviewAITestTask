from fastapi import APIRouter, HTTPException
from app.services.github import fetch_repo, fetch_repo_json
from app.services.gpt import analyze_code, extract_review_data
from loguru import logger

router = APIRouter()

@router.post("/review")
async def review_code(assignment_description: str = "that is mvp of the project, that have to load all files in github repo and analyze it",
                      github_repo_url: str = "https://github.com/rykovlad/CodeReviewAITestTask.git",
                      candidate_level: str = "Junior"):
    """
    :param assignment_description: a brief description of the project
    :param github_repo_url: str, that have owner and repo_name in it
    :param candidate_level: Junior, Middle or Senior only
    :return:
    """
    try:
        repo_content = await fetch_repo(github_repo_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem with github parsing\n" + str(e))

    try:
        review = await analyze_code(assignment_description, repo_content, candidate_level)
        return {"result": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Problem with openAI\n" + str(e))
