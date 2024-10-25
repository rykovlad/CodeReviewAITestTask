# Code Review AI Test Task

This project implements automated code loading from GitHub and analyzes it using ChatGPT based on specified criteria.

## Instructions

### 1. Clone the Repository

Clone the project to your local machine:

```bash
git clone <your_repository_URL>
cd <repository_folder_name>
```

### 2. Set Up Environment Variables
Create a .env file in the root directory of the project and set the following variables:

```makefile
OPENAI_API_KEY=<your_OpenAI_API_key>
GITHUB_API_KEY=<your_GitHub_API_key>
```
### 3. Check Your OpenAI Account Balance
Ensure you have sufficient funds in your OpenAI account to use the API.

### 4. Modify Configuration (Optional)
If needed, modify the variables in config.py according to your requirements.

### 5. Run the Project
Execute the following command in your terminal within the project directory:

```bash
docker-compose up
```
### 6. Access the API Documentation
Open your browser and navigate to:
http://localhost:8000/docs

### 7. Test the Application
Try testing the application using the following data:

```json
{
  "assignment_description": "The project should load code from GitHub and analyze it with ChatGPT by certain criteria.",
  "github_repo_url": "https://github.com/rykovlad/CodeReviewAITestTask",
  "candidate_level": "Junior"
}
```
### Additional Information
To use Redis, make sure the Docker container for Redis is running alongside the API.
If you encounter any errors, check the logs in the terminal for further information.
