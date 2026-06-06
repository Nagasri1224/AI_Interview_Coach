import whisper

print("Loading Whisper Model...")

model = whisper.load_model("base")

print("Transcribing Audio...")

result = model.transcribe("answer.wav")

print("\nTranscript:")
print(result["text"])