def calculate_readiness(
    eye_contact_score,
    attention_score,
    filler_penalty
):

    communication_score = max(
        0,
        100 - filler_penalty
    )

    readiness_score = round(

        (
            communication_score +
            eye_contact_score +
            attention_score

        ) / 3,

        2

    )

    if readiness_score >= 85:

        status = "READY FOR INTERVIEWS"

    elif readiness_score >= 70:

        status = "NEEDS MORE PRACTICE"

    else:

        status = "NEEDS SIGNIFICANT IMPROVEMENT"

    return (
        communication_score,
        readiness_score,
        status
    )