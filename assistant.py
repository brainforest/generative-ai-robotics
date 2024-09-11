import pyaudio
import subprocess
import wave
import time
import speech_recognition as sr
import struct 
from io import BytesIO
from pathlib import Path
from openai import OpenAI
from pixels import Pixels
import RPi.GPIO as GPIO
import io
import os
import json
import threading
import random

debug_audio = False
# Pixel animations during record, speak and think
pixels = Pixels()

# Button definition
BUTTON = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN)
button_pressed = False

# Respeaker settings
RESPEAKER_RATE = 16000  # Sample rate
RESPEAKER_CHANNELS = 2  # Number of channels
RESPEAKER_WIDTH = 2  # Sample width in bytes
RESPEAKER_INDEX = 1  # Input device ID
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 10  # Duration of recording
SILENCE_THRESHOLD = 7500  # Sessizlik eşiği (örnekleme değerleri toplamı)
SILENCE_DURATION = 2  # Sessizlik süresi (saniye)
TRESHOLD = (RESPEAKER_RATE / CHUNK * SILENCE_DURATION) 

# Initialize PyAudio
p = pyaudio.PyAudio()

question_headers = ["7 yaşındaki çocuk için eğlenceli bir cevap ver: "] 

max_history_length = 100
# File to store conversation history
history_file = "conversation_history.json"

# Function to load conversation history from a file
def load_history():
    if os.path.exists(history_file) and os.stat(history_file).st_size != 0:
        with open(history_file, 'r',encoding='utf-8') as file:
            history = json.load(file)
            # Keep only the last 100 messages
            if len(history) > max_history_length:
                history = history[-max_history_length:]
            return history
    return [{"role": "system", "content": "7 yaşındaki çocuk için eğlenceli bir şekilde kısa cevap ver: ."}]

# Initialize the conversation history by loading from file
conversation_history = load_history()

# Function to save conversation history to a file
def save_history(history):
    with open(history_file, 'w', encoding='utf-8') as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


# Function to add a message to the conversation history
def add_to_history(role, content):
    conversation_history.append({"role": role, "content": content})
    # Keep only the last 100 messages
    if len(conversation_history) > max_history_length:
        conversation_history.pop(0)
    # Save history to file after each addition
    save_history(conversation_history)

# Listen speaker 
def _listen():

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

     silence_counter = 0
     frames = []
     # Record audio in chunks
     for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
         data = stream.read(CHUNK)
         frames.append(data)

         # Veriyi çözümle ve ortalama ses seviyesini hesapla
         audio_data = struct.unpack(str(len(data)//2) + 'h', data)
         audio_level = sum(abs(sample) for sample in audio_data) / len(audio_data)

         if (debug_audio):
            print("> audio level" , audio_level)

         # Sesin sessizlik olup olmadığını kontrol et
         if audio_level < SILENCE_THRESHOLD:
             silence_counter += 1
         else:
             silence_counter = 0

         if (debug_audio):
             print("> silence counter " , silence_counter)

         # Sessizlik süresi dolduysa kaydı durdur
         if silence_counter > int(TRESHOLD):
             print("* Sessizlik tespit edildi, kayıt durduruluyor.")
             break

     print("* done recording")

     # Stop and close the stream
     stream.stop_stream()
     stream.close()
     # p.terminate()

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

     question = ""
     # Convert the speech to text using Google's API
     try:
        # Get the result from Google Speech Recognition
        question = recognizer.recognize_google(audio, language="tr-TR",show_all=False)
        print("User: ", question)
        return question

     except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
     except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service")

     return " "


# OpenAI API to use generative ChatGPT
def think_and_answer(question):
 
    global button_pressed
 
    button_pressed = False

    pixels.think()
    client = OpenAI()

    header = random.choice(question_headers)

    print(">> Question Header : " , header)

    add_to_history("user", header + question)

    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=conversation_history
    )

    # Extract the assistant's message and add it to the history
    answer = completion.choices[0].message.content
    add_to_history("assistant", answer)

    print(answer)

    pixels.speak()

    stream = p.open(format=8, channels=1, rate=24_000, output=True)

    with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="onyx",
            input=answer,
            response_format="pcm") as response:
               for chunk in response.iter_bytes(1024):
                   if (button_pressed):
                       break
                   stream.write(chunk)


    pixels.off()
    time.sleep(1)

    return " "

def _speak(speech_file_path):
    pixels.speak()
    # MP3 dosyasını mpg123 ile oynatın
    subprocess.run([ "mpg123", str(speech_file_path) ])
    pixels.off()

def monitor_button():
    global button_pressed
    while True:
        state = GPIO.input(BUTTON)
        if not state:  # Assuming the button is active low
            button_pressed = True
        time.sleep(0.01)

print("wakeup...")
pixels.wakeup()
time.sleep(3)

print("Ready...")
_speak("./welcome.mp3")

# Start the button monitoring thread
button_thread = threading.Thread(target=monitor_button, daemon=True)
button_thread.start()

# Main loop
while True:
    if (button_pressed):
        question = _listen()
        if (len(question) > 3):
            answer = think_and_answer(question)
            time.sleep(0.01)
