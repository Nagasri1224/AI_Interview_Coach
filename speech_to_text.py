import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

model = whisper.load_model("base")

STOP_SPEECH = False


def stop_speech():

    global STOP_SPEECH

    STOP_SPEECH = True

    sd.stop()
    fs=44100


def get_speech_text():

    global STOP_SPEECH

    STOP_SPEECH = False

    fs = 44100

    print("\nListening...")

    recorded_audio = []

    def audio_callback(indata, frames, time, status):

        if STOP_SPEECH:
            raise sd.CallbackStop()

        recorded_audio.append(
            indata.copy()
        )

    try:

        with sd.InputStream(
            samplerate=fs,
            channels=1,
            dtype="int16",
            callback=audio_callback
        ):

            while not STOP_SPEECH:
                sd.sleep(100)

    except Exception:
        pass

    if len(recorded_audio) == 0:

        return "No answer recorded"

    audio = np.concatenate(
        recorded_audio,
        axis=0
    )

    write(
        "answer.wav",
        fs,
        audio
    )

    print("Transcribing...")

    result = model.transcribe(
        "answer.wav"
    )

    return result["text"]