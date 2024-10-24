import json

from pprint import pprint

from fastapi import HTTPException
from openai import OpenAI
from starlette.responses import PlainTextResponse

from app.services.github import fetch_repo_json
from app.core.config import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

async def analyze_code(assignment_description: str, repo_content: dict, candidate_level: str) -> dict:
    prompt = generate_prompt(repo_content, candidate_level, assignment_description)

    # import tiktoken
    #
    # def count_tokens(_text: str, model: str = "gpt-4") -> int:
    #     encoding = tiktoken.encoding_for_model(model)
    #     tokens = encoding.encode(_text)
    #     return len(tokens)
    #
    # tokens_count = count_tokens(prompt)
    # print(f"Number of tokens: {tokens_count}")

    # try:
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a code reviewer"},
            {"role": "user", "content": prompt}
            # {"role": "user", "content": "print(10)"}
        ],
    )
    pprint(response)
    answer = response.choices[0].message.content

    print(answer)

    return extract_review_data(answer)

    # except Exception as e:
    #     print(e)
    #     raise HTTPException(status_code=500, detail="Failed to analyze the code")



def generate_prompt(repo_content: dict, candidate_level: str, assignment_description: str) -> str:
    files = ''
    for file_name, file in repo_content.items():
        print(file_name)
        files += file_name + ":\n"
        files += file + "\n"

    return f"""Please analyze the following files for a {candidate_level} level candidate, assignment description:
    {assignment_description}            
         Make structured report in JSON format with the following fields:
    - 'issues': A list of specific issues found in the code in format dictionary with "file" and  "description" keys, 
    also "file" value is str of filename, and "description" value is list of str of issues and number of line with that issue
    - 'rating': A rating of the candidate's performance (e.g., 1-5 or a detailed textual description) in forman "n/5"
    - 'conclusion': A final assessment of the code quality, areas for improvement and and compliance with the assignment description
    - 'analyzed_files': List of all files in promt
    
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
      "rating": "n/5",
      "conclusion": "Final assessment of the code quality and areas for improvement",
      "analyzed_files": ["file1.py", "file2.py", ...]
    }}

    
    Project:
    
    {files}    
    """


# Функція для обробки результатів з OpenAI
def extract_review_data(text: str) -> dict:
    if text[:8]=="```json\n" and text[-3:]=="```":
        text = text[8:-3]

    data_dict = json.loads(text)
    pprint(data_dict)

    with open("last_answer.json", 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

    return data_dict


if __name__ == '__main__':
    async def review_code(assignment_description: str = "",
                    github_repo_url: str = "https://github.com/rykovlad/test_task_204.git",
                    candidate_level: str = "Junior"):
        try:
            repo_content = await fetch_repo_json(github_repo_url)  # switch to fetch_repo() for real tests

            review = await analyze_code(assignment_description, repo_content, candidate_level)

            return {"result": review}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))



    import asyncio
    asyncio.run(review_code())
