import pyaudio
import speech_recognition as sr
import pyttsx3
import random

# Initialize recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# Greetings to choose from
greetings = ["Hello, how can I assist you?", "Hi there! What do you need?", "Hey! How can I help?"]

# PyAudio settings
RESPEAKER_RATE = 16000  # Sample rate
RESPEAKER_CHANNELS = 1  # Mono channel for recognizer
RESPEAKER_WIDTH = 2  # Sample width in bytes
CHUNK = 1024  # Buffer size

def listen_for_wake_word(source):
    print("Listening for 'Hello'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hello" in text.lower():
                print("Wake word detected.")
                engine.say(random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            # If speech is unintelligible, just continue listening
            pass

def listen_and_respond(source):
    print("Listening for a command...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            # Process the command here, for now just acknowledge it
            engine.say(f"You said: {text}")
            engine.runAndWait()
            break
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")

def main():
    # Set up the microphone source
    with sr.Microphone(sample_rate=RESPEAKER_RATE) as source:
        r.adjust_for_ambient_noise(source)
        listen_for_wake_word(source)

if __name__ == "__main__":
    main()

