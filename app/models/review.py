from pydantic import BaseModel, HttpUrl, Field
from typing import Literal

class ReviewRequest(BaseModel):
    assignment_description: str = Field(..., title="Assignment Description", example="Write a function to reverse a string")
    github_repo_url: HttpUrl = Field(..., title="GitHub Repository URL", example="https://github.com/example/repo")
    candidate_level: Literal['Junior', 'Middle', 'Senior'] = Field(..., title="Candidate Level")

class ReviewResponse(BaseModel):
    analyzed_files: list[str] = Field(..., title="Found and analyzed files", example=["main.py", "utils.py"])
    issues: list[dict] = Field(..., title="Downsides/Comments")
    rating: str = Field(..., title="Rating", example="4/5 for a Junior level candidate")
    conclusion: str = Field(..., title="Conclusion", example="Good implementation but needs better structure")
