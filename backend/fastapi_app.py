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
    user_message: str

class GroqResponse(BaseModel):
    # match_score: int
    # feedback: list
    # updated_resume: str
    coach_message: str

@app.post("/hey_coach", response_model=GroqResponse)
def analyze_job_resume(request: AnalyzeRequest):
    # return GroqResponse(
    #     coach_message="Hello, I am your job hunt coach. I am here to help you improve your resume and prepare for job interviews. Please provide me with your job description and resume."
    # )
    if not request.job_description or not request.resume:
        logger.error("Invalid input: Job description or resume is missing.")
        raise HTTPException(status_code=400, detail="Invalid input")


    system_message = f"""
    You are a senior job search coach at a career services company.
    You help clients improve their resumes to better match job descriptions.
    You help clients prepare for their job interviews based on given job description and resume.
    You help clients to improve their skills and experiences to better match the job requirements.
    Do not suggest to add new things to resume, only suggest to enhance the existing resume.
    If skills are missing, ask users to gain certifications or hands on experience in those skills.

    To enhance the resume, Make sure this is the best resume ever but don't make up any information. 
    Ask users which sections they want to update and go through suggestions one section at a time. 
    Answer any follow up questions and tweak the suggestions

    Job Description:
    {request.job_description}

    Resume:
    {request.resume}

    DO NOT include job description or resume in your response to the user.
    """

    user_message = f"""
    User has asked following question: {request.user_message}

    Respond to user's questions succinctly, ask follow up questions if required or there is any ambiguity.

    """

    client = Groq()
    # client = instructor.from_groq(Groq(), mode=instructor.Mode.JSON)

    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        # response_model=GroqResponse,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
    )

    if not response:
        logger.error("GroqCloud request failed")
        raise HTTPException(status_code=500, detail="GroqCloud request failed")

    
    logger.info("Received response from GroqCloud: %s", response)

    return GroqResponse(
        coach_message=response.choices[0].message.content,
    )