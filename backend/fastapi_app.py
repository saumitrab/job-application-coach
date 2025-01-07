from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from groq import Groq
import instructor

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyzeRequest(BaseModel):
    job_description: str
    resume: str

class GroqResponse(BaseModel):
    match_score: int
    feedback: list
    updated_resume: str

@app.post("/analyze_job_resume", response_model=GroqResponse)
def analyze_job_resume(request: AnalyzeRequest):
    if not request.job_description or not request.resume:
        logger.error("Invalid input: Job description or resume is missing.")
        raise HTTPException(status_code=400, detail="Invalid input")


    system_message = """
Using the resume and job description below, tailor the resume to highlight the most relevant areas.
adjust and enhance the resume content. Make sure this is the best resume ever but don't make up any information. 
Update every section, including the initial summary, work experience, skills, and education. 
Better reflect the candidate's abilities and how it matches the job posting.

expected output: An updated resume that effectively highlights the candidate's qualifications and experiences relevant to the job.

Return the resume in the html format. 
keep the style simple and similar to the original resume. 
Do not create tables or use complex formatting.
Ensure the resume is easy to read and professional.
"""

    user_message = f"""
Job Description:
{request.job_description}

Resume:
{request.resume}
"""

    # client = Groq(api_key=groqcloud_api_key)
    client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON)

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        response_model=GroqResponse,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
    )

    if not response:
        logger.error("GroqCloud request failed")
        raise HTTPException(status_code=500, detail="GroqCloud request failed")

    
    logger.info("Received response from GroqCloud: %s", response.updated_resume)

    return GroqResponse(
        match_score=response.match_score,
        feedback=response.feedback,
        updated_resume=response.updated_resume
    )