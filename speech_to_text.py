import whisper
import sounddevice as sd
from scipy.io.wavfile import write

model = whisper.load_model("base")

def get_speech_text():

    fs = 44100

    print("\nListening...")

    audio = sd.rec(
        int(10 * fs),
        samplerate=fs,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    write("answer.wav", fs, audio)

    print("Transcribing...")

    result = model.transcribe("answer.wav")

    return result["text"]