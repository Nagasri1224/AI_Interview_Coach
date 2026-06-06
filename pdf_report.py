from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from datetime import datetime

from sympy import content


def create_pdf(report):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    pdf = SimpleDocTemplate(
        f"reports/Interview_Report_{timestamp}.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    # ==========================
    # Title
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
    # Interview Summary
    # ==========================

    content.append(
        Paragraph(
            "<b>INTERVIEW SUMMARY</b>",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Final Score:</b> {report['final_score']}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Eye Contact Score:</b> {report['eye_contact_score']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Attention Score:</b> {report['attention_score']}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Filler Penalty:</b> {report['filler_penalty']}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 15)
    )

    # ==========================
    # Interview Readiness
    # ==========================

    content.append(
        Paragraph(
            "<b>INTERVIEW READINESS</b>",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Communication Score:</b> {report.get('communication_score', 'N/A')}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Readiness Score:</b> {report.get('readiness_score', 'N/A')}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Status:</b> {report.get('status', 'N/A')}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    # ==========================
    # Questions Section
    # ==========================

    for i, item in enumerate(
        report["questions"],
        start=1
    ):

        content.append(
            Paragraph(
                f"Question {i}",
                styles["Heading1"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Question:</b> {item['question']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Answer:</b> {item['answer']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Answer Time:</b> {item['answer_time']} seconds",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Words Spoken:</b> {item['words_spoken']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Filler Count:</b> {item['filler_count']}",
                styles["Normal"]
            )
        )

        content.append(
            Paragraph(
                f"<b>Penalty:</b> {item['penalty']}",
                styles["Normal"]
            )
        )
        content.append(
            Paragraph(
                f"<b>Eye Contact Score:</b> {item.get('eye_contact_score', 'N/A')}%",
                styles["Normal"]
            )
        )
        content.append(
            Paragraph(
                f"<b>Attention Score:</b> {item.get('attention_score', 'N/A')}%",
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 10)
        )

        # ==========================
        # AI Feedback
        # ==========================

        content.append(
            Paragraph(
                "<b>AI FEEDBACK</b>",
                styles["Heading2"]
            )
        )

        feedback = item["ai_feedback"]

        feedback = feedback.replace(
            "\n",
            "<br/>"
        )

        content.append(
            Paragraph(
                feedback,
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 20)
        )

    pdf.build(content)

    print(
        "PDF Report Generated Successfully"
    )