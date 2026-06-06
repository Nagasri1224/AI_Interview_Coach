from gemini_feedback import get_feedback

question = "Tell me about yourself"

answer = """
My name is Nagasri.
I am a third year AIML student.
I have worked on a Garbage Classification project.
"""

feedback = get_feedback(
    question,
    answer
)

print(feedback)