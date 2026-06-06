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

def get_feedback(question, answer):

    prompt = f"""
You are an expert interview evaluator.

Question:
{question}

Answer:
{answer}

Evaluate the answer and provide:

1. Strengths
2. Weaknesses
3. Communication Score (/10)
4. Confidence Score (/10)
5. Suggestions for improvement

Keep the response concise.
"""

    response = model.generate_content(prompt)

    return response.text