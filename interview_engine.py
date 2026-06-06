import threading

from speech_to_text import get_speech_text
from camera_live import get_live_camera_scores


def run_question():

    answer = None
    eye_score = None
    attention_score = None

    def speech_worker():

        nonlocal answer

        answer = get_speech_text()

    def camera_worker():

        nonlocal eye_score
        nonlocal attention_score

        eye_score, attention_score = (
            get_live_camera_scores()
        )

    t1 = threading.Thread(
        target=speech_worker
    )

    t2 = threading.Thread(
        target=camera_worker
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    return (
        answer,
        eye_score,
        attention_score
    )