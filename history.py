import os
import json

REPORTS_FOLDER = "reports"

reports = []

# Read all report files
for file in os.listdir(REPORTS_FOLDER):

    if file.endswith(".json"):

        path = os.path.join(
            REPORTS_FOLDER,
            file
        )

        try:

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as f:

                report = json.load(f)

                if "final_score" in report:

                    report["file_name"] = file

                    reports.append(report)

        except Exception as e:

            print(
                f"Skipping {file}:",
                e
            )

if len(reports) == 0:

    print("No Valid Interview Reports Found")

else:

    print("=" * 60)
    print("INTERVIEW HISTORY")
    print("=" * 60)

    scores = []

    for i, report in enumerate(reports):

        score = report.get(
            "final_score",
            0
        )

        scores.append(score)

        print(f"\nInterview #{i+1}")

        print(
            "File :",
            report.get(
                "file_name",
                "Unknown"
            )
        )

        if "date" in report:

            print(
                "Date :",
                report["date"]
            )

        print(
            "Score:",
            score
        )

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    best_score = max(scores)

    average_score = round(
        sum(scores) / len(scores),
        2
    )

    latest_score = scores[-1]

    first_score = scores[0]

    improvement = round(
        latest_score - first_score,
        2
    )

    print(
        "Total Interviews :",
        len(scores)
    )

    print(
        "Best Score       :",
        best_score
    )

    print(
        "Average Score    :",
        average_score
    )

    print(
        "Latest Score     :",
        latest_score
    )

    print(
        "Improvement      :",
        improvement
    )

    latest_report = reports[-1]

    print("\n" + "=" * 60)
    print("LATEST INTERVIEW")
    print("=" * 60)

    print(
        "Eye Contact Score :",
        latest_report.get(
            "eye_contact_score",
            "N/A"
        )
    )

    print(
        "Attention Score   :",
        latest_report.get(
            "attention_score",
            "N/A"
        )
    )

    print(
        "Filler Penalty    :",
        latest_report.get(
            "filler_penalty",
            "N/A"
        )
    )

    print(
        "Final Score       :",
        latest_report.get(
            "final_score",
            "N/A"
        )
    )