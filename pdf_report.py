from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime
import os


def create_pdf(report):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"reports/Interview_Report_{timestamp}.pdf"
    )

    pdf = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    # ==========================
    # TITLE
    # ==========================

    content.append(
        Paragraph(
            "AI INTERVIEW COACH REPORT",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==========================
    # SUMMARY
    # ==========================

    content.append(
        Paragraph(
            "INTERVIEW SUMMARY",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Final Score: {report.get('final_score', 0)}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Communication Score: {report.get('communication_score', 0)}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Readiness Score: {report.get('readiness_score', 0)}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Status: {report.get('status', 'N/A')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Filler Penalty: {report.get('filler_penalty', 0)}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==========================
    # QUESTIONS
    # ==========================

    content.append(
        Paragraph(
            "INTERVIEW QUESTIONS",
            styles["Heading1"]
        )
    )

    questions = report.get(
        "questions",
        []
    )

    for i, question in enumerate(
        questions,
        start=1
    ):

        content.append(
            Paragraph(
                f"Question {i}",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                str(question),
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

    pdf.build(content)

    print(
        f"PDF Generated: {filename}"
    )

    return filename