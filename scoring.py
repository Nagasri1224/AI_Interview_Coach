def calculate_score(
    eye_contact,
    attention,
    filler_penalty
):

    speech_score = 100 - filler_penalty

    final_score = (
        eye_contact * 0.4 +
        attention * 0.4 +
        speech_score * 0.2
    )

    return round(final_score, 2)
def calculate_score(
    eye_contact,
    attention,
    filler_penalty
):

    speech_score = 100 - filler_penalty

    final_score = (
        eye_contact * 0.4 +
        attention * 0.4 +
        speech_score * 0.2
    )

    return round(final_score, 2)

