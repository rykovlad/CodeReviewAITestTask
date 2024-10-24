import base64

import httpx
from fastapi import HTTPException
from loguru import logger

from app.core.config import config


async def get_repo_contents(api_url, headers):
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Fetching folder with url = {api_url}")
            response = await client.get(api_url, headers=headers)

        if response.status_code != 200:
            logger.error(f"Error: {response.status_code}")
            return None
        return response.json()
    except HTTPException as e:
        logger.error("api_url = " + api_url)
        logger.error(e)

async def fetch_repo(github_repo_url: str) -> dict:
    headers = {
        "Authorization": f"token {config.GITHUB_API_KEY}"
    }

    owner, repo = github_repo_url.split("/")[-2:]
    repo = repo.replace(".git", "")

    base_api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    logger.info(f"Trying get {owner}`s repo named {repo}")

    async def recursive_fetch_files(api_url, repo_data):
        files = await get_repo_contents(api_url, headers)

        for file in files:
            if file['type'] == 'file':
                file_content_url = file['url']
                async with httpx.AsyncClient() as _client:
                    file_content_response = await _client.get(file_content_url, headers=headers)

                if file_content_response.status_code == 200:
                    file_data = file_content_response.json()
                    content = base64.b64decode(file_data['content']).decode('utf-8')
                    logger.info(f"Successfully added {file['path']}")
                    repo_data[file['path']] = content
                else:
                    logger.error(f"Error getting file {file['path']}: {file_content_response.status_code}")

            elif file['type'] == 'dir':
                dir_url = file['url']
                await recursive_fetch_files(dir_url, repo_data)

    repo_data = {}
    await recursive_fetch_files(base_api_url, repo_data)

    with open("last_repo.json", 'w', encoding='utf-8') as f:
        import json
        json.dump(repo_data, f, ensure_ascii=False, indent=4)

    return repo_data

async def fetch_repo_json(github_repo_url: str) -> dict:
    '''
    test function just to write other code without fetching repo from git

    :param github_repo_url: no sense
    :return:
    '''
    import os
    # file_path = "/last_repo.json"
    file_path = os.path.join(os.path.dirname(__file__), "last_repo.json")
    import json
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")
        return None
    except json.JSONDecodeError:
        print(f"Помилка декодування JSON у файлі {file_path}.")
        return None


if __name__ == '__main__':
    import asyncio
    asyncio.run(fetch_repo("https://github.com/SAYREKAS/CodeReviewAITool.git"))
