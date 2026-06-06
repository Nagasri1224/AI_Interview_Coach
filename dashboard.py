import os
import json

REPORTS_FOLDER = "reports"

scores = []

for file in os.listdir(REPORTS_FOLDER):

    if file.endswith(".json"):

        path = os.path.join(
            REPORTS_FOLDER,
            file
        )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            report = json.load(f)

            scores.append(
                report["final_score"]
            )

if len(scores) == 0:

    print("No Reports Found")

else:

    print("=" * 50)
    print("INTERVIEW DASHBOARD")
    print("=" * 50)

    print(
        "Total Interviews :",
        len(scores)
    )

    print(
        "Best Score       :",
        max(scores)
    )

    print(
        "Average Score    :",
        round(
            sum(scores) / len(scores),
            2
        )
    )

    print(
        "Latest Score     :",
        scores[-1]
    )