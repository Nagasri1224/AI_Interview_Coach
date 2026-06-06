import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100

print("Recording... Speak now")

audio = sd.rec(
    int(10 * fs),
    samplerate=fs,
    channels=1
)

sd.wait()

write("answer.wav", fs, audio)

print("Recording Saved")