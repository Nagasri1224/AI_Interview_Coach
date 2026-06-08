from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from resume_parser import extract_resume_text
from resume_questions import generate_questions
from pydantic import BaseModel
from interview_engine import run_question
from gemini_feedback import get_feedback
from pdf_report import create_pdf
from camera_live import stop_camera
from speech_to_text import stop_speech
from fastapi.responses import FileResponse
import os
import glob


from filler_detector import analyze_fillers
from readiness import calculate_readiness

app = FastAPI()
class AnalysisRequest(BaseModel):
    transcript: str
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "AI Interview Coach API Running"
    }


@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...)
):

    # Save uploaded PDF

    pdf_path = file.filename

    with open(
        pdf_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )

    # Extract resume text

    resume_text = extract_resume_text(
        pdf_path
    )

    # Generate questions

    try:

        questions = generate_questions(
            resume_text
        )

    except Exception as e:

        print("Gemini Error:", e)

        questions = [

            "Tell me about yourself",

            "Why should we hire you?",

            "What are your strengths?",

            "What are your weaknesses?",

            "Describe your Garbage Classification project",

            "Explain CNN and why you used it",

            "Describe your Fake News Detection project",

            "What challenges did you face during project development?",

            "Where do you see yourself in 5 years?",

            "Do you have any questions for us?"
        ]

    return {

        "filename": file.filename,

        "resume_text": resume_text,

        "questions": questions

    }
from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    question: str
    answer: str


@app.post("/feedback")
def feedback(data: FeedbackRequest):

    try:

        result = get_feedback(
            data.question,
            data.answer
        )

        return {
            "feedback": result
        }

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "feedback":
            "Gemini quota exceeded or API error."
        }
@app.post("/analyze-answer")
def analyze_answer(data: AnalysisRequest):
    print("TRANSCRIPT:",data.transcript)

    filler_count, penalty = analyze_fillers(
        data.transcript
    )

    word_count = len(
        data.transcript.split()
    )

    communication_score = min(
        word_count * 5,
        100
    )

    readiness_score = max(
        (
            communication_score
            - penalty
        ),
        0
    )

    if readiness_score >= 80:
        status = "READY FOR INTERVIEWS"

    elif readiness_score >= 60:
        status = "NEEDS IMPROVEMENT"

    else:
        status = "MORE PRACTICE REQUIRED"

    return {

        "filler_count":
        filler_count,

        "penalty":
        penalty,

        "communication_score":
        communication_score,

        "readiness_score":
        readiness_score,

        "status":
        status
    }

    return {

        "filler_count":
        filler_count,

        "penalty":
        penalty,

        "communication_score":
        communication_score,

        "readiness_score":
        readiness_score,

        "status":
        status
    }
@app.post("/final-score")
def final_score(data: AnalysisRequest):

    filler_count, penalty = analyze_fillers(
        data.transcript
    )

    word_count = len(
        data.transcript.split()
    )

    communication_score = min(
        word_count * 5,
        100
    )

    readiness_score = max(
        communication_score - penalty,
        0
    )

    final_score = round(
        (
            communication_score * 0.6
            +
            readiness_score * 0.4
        ),
        2
    )

    return {
        "score": final_score
    }
from fastapi.responses import FileResponse
import os

@app.get("/download-report")
def download_report():

    report_path = "reports/latest_report.pdf"

    if os.path.exists(report_path):

        return FileResponse(
            report_path,
            media_type="application/pdf",
            filename="Interview_Report.pdf"
        )

    return {
        "error": "No report found"
    }
from pydantic import BaseModel

class ReportRequest(BaseModel):

    final_score: float=0
    eye_contact_score: float=0

    attention_score: float=0

    communication_score: float=0

    readiness_score: float=0

    status: str="N/A"

    filler_penalty: int=0

    questions: list =[]
@app.post("/generate-report")
def generate_report(data: ReportRequest):

    report = {

        "final_score":
        data.final_score,

        "eye_contact_score":
        data.eye_contact_score,

        "attention_score":
        data.attention_score,

        "filler_penalty":
        data.filler_penalty,

        "communication_score":
        data.communication_score,

        "readiness_score":
        data.readiness_score,

        "status":
        data.status,

        "questions":
        data.questions
    }

    create_pdf(report)

    pdf_files = glob.glob(
        "reports/*.pdf"
    )

    latest_pdf = max(
        pdf_files,
        key=os.path.getctime
    )

    return FileResponse(
        latest_pdf,
        media_type="application/pdf",
        filename="Interview_Report.pdf"
    )
    
@app.get("/camera-analysis")
def camera_analysis():

    answer, eye_score, attention_score = (
        run_question()
    )
    print("Answer:", answer)
    print("Eye Score:", eye_score)
    print("Attention Score:", attention_score)

    return {

        "answer":
        answer,

        "eye_score":
        eye_score,

        "attention_score":
        attention_score
    }
@app.get("/stop-interview")
def stop_interview():

    stop_camera()
    stop_speech()
    return {
        "message": "Interview stopped"
    }