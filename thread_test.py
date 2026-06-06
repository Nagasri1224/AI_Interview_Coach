import threading

from speech_to_text import get_speech_text
from camera_live import get_live_camera_scores

answer = None
eye_score = None
attention_score = None


def speech_worker():

    global answer

    answer = get_speech_text()


def camera_worker():

    global eye_score
    global attention_score

    eye_score, attention_score = (
        get_live_camera_scores()
    )


t1 = threading.Thread(
    target=speech_worker
)

t2 = threading.Thread(
    target=camera_worker
)

print("Starting Interview...")

t1.start()
t2.start()

t1.join()
t2.join()

print("\nTRANSCRIPT:")
print(answer)

print("\nEye Contact:", eye_score)

print("Attention:", attention_score)