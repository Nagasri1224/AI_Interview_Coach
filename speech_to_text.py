def get_speech_text():
    
    fs = 44100

    print("\nListening...")

    audio = sd.rec(
        int(60 * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write(
        "answer.wav",
        fs,
        audio
    )

    print("Transcribing...")

    result = model.transcribe(
        "answer.wav"
    )

    print("\nTRANSCRIBED:")
    print(result["text"])

    return result["text"]