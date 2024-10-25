import json

from pprint import pprint

from loguru import logger

from fastapi import HTTPException
from openai import OpenAI, OpenAIError, RateLimitError, AuthenticationError, APIConnectionError

from app.core.config import config
from app.models.review import ReviewResponse

client = OpenAI(api_key=config.OPENAI_API_KEY)

async def analyze_code(assignment_description: str, repo_content: dict, candidate_level: str) -> ReviewResponse:
    """
    Analyzes code based on the assignment description, repository content, and candidate level.

    The function generates a prompt for code analysis, sends it to the GPT model via API to review the code and
    provide feedback.
    It processes the response and returns the result in a dictionary format containing identified issues and the
    candidate's evaluation.

    :param assignment_description: A description of the task the candidate is expected to complete (str).
    :param repo_content: A dictionary where keys are file names and values are the content of those files (dict).
    :param candidate_level: The experience level of the candidate (e.g., junior, mid, senior) (str).

    :return: A dictionary with the analysis results, including issues and the candidate's performance rating.
    """
    prompt = generate_prompt(repo_content, candidate_level, assignment_description)

    try:
        response = client.chat.completions.create(
            model=config.CHAT_GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a code reviewer"},
                {"role": "user", "content": prompt}
            ],
        )
        logger.info(response)

        answer = response.choices[0].message.content
        logger.info(answer)

        return extract_review_data(answer)

    except AttributeError as e:
        logger.error(f"Attribute error: {str(e)}")
        raise HTTPException(status_code=500, detail="Malformed response structure from OpenAI API.")

    except AuthenticationError as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid OpenAI API credentials")

    except RateLimitError as e:
        logger.error(f"Rate limit error: {str(e)}")
        raise HTTPException(status_code=429, detail="OpenAI API rate limit exceeded. Please try again later.")

    except APIConnectionError as e:
        logger.error(f"API connection error: {str(e)}")
        raise HTTPException(status_code=503, detail="Failed to connect to OpenAI API. Please check your network.")

    except OpenAIError as e:
        # Catch any other OpenAI-related errors
        logger.error(f"OpenAI error: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the code analysis.")

    # General exception handling
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze the code")


def generate_prompt(repo_content: dict, candidate_level: str, assignment_description: str) -> str:
    """
    Generate prompt with your params

    :param repo_content: dict {"filename.py": "print(code)"}
    :param candidate_level: Junior, Middle or Senior levels
    :param assignment_description:  a brief description of the project
    :return: full text of prompt
    """
    files = ''
    for file_name, file in repo_content.items():
        files += file_name + ":\n"
        files += file + "\n"

    return f"""Please analyze the following files for a {candidate_level} level candidate, assignment description:
    {assignment_description}            
         Make structured report in JSON format with the following fields:
    - 'issues': A list of specific issues found in the code in format dictionary with "file" and  "description" keys, 
    also "file" value is str of filename, and "description" value is list of str of issues and number of line with that issue
    - 'rating': A rating of the candidate's performance (e.g., 1-5 or a detailed textual description) in forman "n/5"
    - 'conclusion': A final assessment of the code quality, areas for improvement, suggest improvements and compliance 
    with the assignment description 
    - 'analyzed_files': List of **all** files in prompt
    
    Provide a **strict JSON** response. **Do not** include any additional text or explanations, only return the JSON object.

    The JSON structure should follow this format:
    ```json
    {{
      "issues": [
        {{
          "file": "filename.py",
          "description": [
            "Issue 1 description",
            "Issue 2 description"
          ]
        }},
        ...
      ],
      "rating": "n/5 for a {candidate_level} level candidate",
      "conclusion": "Final large assessment of the code quality and areas for improvement and compliance with the assignment description",
      "analyzed_files": ["file1.py", "file2.py", ...]
    }}

    Project:
    
    {files}    
    """


def extract_review_data(text: str) -> ReviewResponse:
    """
    transform str answer to dict and save it locally(can be commented)

    :param text: answer from openai API
    :return: answer in dict format
    """
    try:
        if text[:8]=="```json\n" and text[-3:]=="```":
            text = text[8:-3]

        data_dict = json.loads(text)
        pprint(data_dict)

        with open("last_answer.json", 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

        return ReviewResponse(
            analyzed_files=data_dict["analyzed_files"],
            issues=data_dict["issues"],
            rating=data_dict["rating"],
            conclusion=data_dict["conclusion"]
        )

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        logger.error(f"JSON decoding error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON format received.")

    except TypeError as e:
        # Handle TypeErrors, such as if the input is not a string
        logger.error(f"Type error: {str(e)}")
        raise HTTPException(status_code=400, detail="Input data is not a valid string.")

    except Exception as e:
        # Catch any other exceptions
        logger.error(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process the response.")
