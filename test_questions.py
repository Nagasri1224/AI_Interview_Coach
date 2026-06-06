from resume_questions import generate_questions

questions = generate_questions(
    "P.NAGASRI RESUME.pdf"
)

for i, q in enumerate(questions, start=1):

    print(f"{i}. {q}")