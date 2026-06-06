from dotenv import load_dotenv
import google.generativeai as genai
import os
load_dotenv()
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

def generate_questions(resume_text):

    prompt = f"""
You are an interviewer.

Based on this resume, generate exactly 10 interview questions.

Resume:
{resume_text}

Return only the questions.
"""

    response = model.generate_content(prompt)

    questions = []

    for line in response.text.split("\n"):
        line = line.strip()

        if line:
            if line[0].isdigit():
    
                dot_index = line.find(".")

                if dot_index != -1:

                    line = line[
                        dot_index + 1:
                    ].strip()
            questions.append(line)

    return questions