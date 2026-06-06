from speech_to_text import get_speech_text
from camera_live import get_live_camera_scores

print("=" * 60)
print("REAL TIME INTERVIEW")
print("=" * 60)

question = "Tell me about yourself"

print("\nQuestion:")
print(question)

input("\nPress Enter to start...")

answer = get_speech_text()

eye_score, attention_score = get_live_camera_scores()

print("\nTRANSCRIPT")
print(answer)

print("\nEye Contact:", eye_score)

print("Attention:", attention_score)