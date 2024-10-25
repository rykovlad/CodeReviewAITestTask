from pydantic import BaseModel, HttpUrl, Field
from typing import Literal

class ReviewRequest(BaseModel):
    assignment_description: str = Field(..., title="Assignment Description", example="Write a function to reverse a string")
    github_repo_url: HttpUrl = Field(..., title="GitHub Repository URL", example="https://github.com/example/repo")
    candidate_level: Literal['Junior', 'Middle', 'Senior'] = Field(..., title="Candidate Level")

class ReviewResponse(BaseModel):
    found_files: list[str] = Field(..., title="Found Files", example=["main.py", "utils.py"])
    downsides: list[str] = Field(..., title="Downsides/Comments", example=["Code duplication", "Inconsistent naming"])
    rating: int = Field(..., title="Rating", ge=1, le=5, example=4)
    conclusion: str = Field(..., title="Conclusion", example="Good implementation but needs better structure")
