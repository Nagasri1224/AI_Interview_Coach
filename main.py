print("MAIN STARTED")
print("CHECK 1")

print("=" * 60)
print("AI INTERVIEW COACH")
print("=" * 60)

print("CHECK 2")
import time
import json
from datetime import datetime

from interview_engine import run_question

from resume_parser import extract_resume_text
print("CHECK 3")
from resume_questions import generate_questions
print("CHECK 5")
resume_text = extract_resume_text(
    "P.NAGASRI RESUME.pdf"
)

questions = generate_questions(
    resume_text
)
print("Generated Questions:", questions)
from speech_to_text import get_speech_text
from filler_detector import analyze_fillers
from scoring import calculate_score
from gemini_feedback import get_feedback
from pdf_report import create_pdf
from readiness import calculate_readiness

print("=" * 60)
print("AI INTERVIEW COACH")
print("=" * 60)

print("Questions:", questions)
print("Length:", len(questions))

total_filler_penalty = 0
total_eye_score = 0
total_attention_score = 0
question_count = 0
# ----------------------------


# ----------------------------
# INTERVIEW
# ----------------------------

interview_data = []

question_number = 1

for question in questions:

    print("\n" + "=" * 60)
    print(f"Question {question_number}")
    print("=" * 60)

    print(question)

    input("\nPress Enter when ready to answer...")

    print("\nRecording Answer...")
    start_time = time.time()
    answer, eye_score, attention_score = (
        run_question()
    )
    total_eye_score += eye_score
    total_attention_score += attention_score
    question_count += 1
    print(
        "\nEye Contact Score:",
        eye_score
    )
    print(
        "Attention Score:",
        attention_score
        )
    end_time = time.time()

    answer_time = round(end_time - start_time)

    print("\nTranscript:")
    print(answer)

    print("\nAnswer Time:", answer_time, "seconds")

    word_count = len(answer.split())

    print("Words Spoken:", word_count)

    filler_count, penalty = analyze_fillers(answer)

    
    total_filler_penalty += penalty
    print("Filler Words:", filler_count)


    if word_count < 10:
        print("DEBUG C")
        print("Feedback: Answer Too Short")

    elif word_count > 100:

        print("Feedback: Answer Too Long")

    else:

        print("Feedback: Good Answer Length")

    print("\nGenerating AI Feedback...")
    print("DEBUG 1")

    try:
        print("DEBUG 2")
        feedback = get_feedback(
            question,
            answer
        )
        print("DEBUG 3")
        print("\nAI Feedback:")
        print(feedback)
        
    except Exception as e:

        print("Gemini Error:", e)

        feedback = """
Strengths:
- Feedback unavailable

Weaknesses:
- Feedback unavailable

Suggestions:
- Gemini quota exceeded or API error occurred.
"""

    interview_data.append({

        "question": question,
        "answer": answer,
        "answer_time": answer_time,
        "words_spoken": word_count,
        "filler_count": filler_count,
        "penalty": penalty,
        "ai_feedback": feedback,
        "eye_contact_score": eye_score,
        "attention_score": attention_score
    })

    choice = input(
        "\nProceed to next question? (y/n): "
    )

    if choice.lower() != "y":
        break
    
    question_number += 1
if question_count > 0:
    eye_contact_score = round(
        total_eye_score / question_count,
        2
    )

    attention_score = round(
        total_attention_score / question_count,
        2
    )

else:

    eye_contact_score = 0
    attention_score = 0

communication_score, readiness_score, status = (
    calculate_readiness(
        eye_contact_score,
        attention_score,
        total_filler_penalty
    )
)
print("Reached Final Scoring")
# ----------------------------
# FINAL SCORING
# ----------------------------
eye_contact_score = round(
    total_eye_score / question_count,
    2
)

attention_score = round(
    total_attention_score / question_count,
    2
)

final_score = calculate_score(
    eye_contact_score,
    attention_score,
    total_filler_penalty
)

print("\n")
print("=" * 60)
print("INTERVIEW REPORT")

print("=" * 60)

print("Eye Contact Score :", eye_contact_score)
print("Attention Score   :", attention_score)
print("Filler Penalty    :", total_filler_penalty)
print("Final Score       :", final_score)
print("\nINTERVIEW READINESS")

print(
    "Communication Score :",
    communication_score
)

print(
    "Readiness Score     :",
    readiness_score
)

print(
    "Status              :",
    status
)

# ----------------------------
# REPORT DATA
# ----------------------------

report = {

    "date": str(datetime.now()),

    "eye_contact_score": eye_contact_score,

    "attention_score": attention_score,

    "filler_penalty": total_filler_penalty,
    "communication_score":
    communication_score,
    "readiness_score":
    readiness_score,
    "status":
    status,

    "final_score": final_score,

    "questions": interview_data

}

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

json_file = (
    f"reports/interview_{timestamp}.json"
)

with open(
    json_file,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        report,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nJSON Report Saved")

# ----------------------------
# PDF REPORT
# ----------------------------

try:

    create_pdf(report)

    print("PDF Report Generated")

except Exception as e:

    print("PDF Generation Error:", e)

print("\nInterview Completed")