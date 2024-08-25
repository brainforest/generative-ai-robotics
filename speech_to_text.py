import pyaudio
import wave
import speech_recognition as sr
from io import BytesIO
from pixels import Pixels
import time

# Respeaker settings
RESPEAKER_RATE = 16000  # Sample rate
RESPEAKER_CHANNELS = 2  # Number of channels
RESPEAKER_WIDTH = 2  # Sample width in bytes
RESPEAKER_INDEX = 1  # Input device ID
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 5  # Duration of recording

pixels = Pixels()
pixels.off()
time.sleep(1)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open a stream for audio input
stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX
)

pixels.listen()

print("* recording")

frames = []

# Record audio in chunks
for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")


# Stop and close the stream
stream.stop_stream()
stream.close()
p.terminate()

pixels.think()

# Save the recorded audio to an in-memory BytesIO stream and add WAV headers
audio_stream = BytesIO()
wf = wave.open(audio_stream, 'wb')
wf.setnchannels(RESPEAKER_CHANNELS)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Reset the stream position to the beginning
audio_stream.seek(0)

# Initialize the recognizer for SpeechRecognition
recognizer = sr.Recognizer()

# Use the recorded audio stream for speech recognition
with sr.AudioFile(audio_stream) as source:
    audio = recognizer.record(source)  # Read the entire audio stream

# Convert the speech to text using Google's API
try:
    # Get the result from Google Speech Recognition
    result = recognizer.recognize_google(audio, language='tr-TR', show_all=False)
    print(result)

except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")


pixels.off()
time.sleep(3)
