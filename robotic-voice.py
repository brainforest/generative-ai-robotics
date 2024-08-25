import pyaudio
import speech_recognition as sr
import pyttsx3
import random

# Initialize recognizer and text-to-speech engine
engine = pyttsx3.init()

# Greetings to choose from
greetings = ["Hello, how can I assist you?", "Hi there! What do you need?", "Hey! How can I help you?","Yes, master I listen you"]

engine.say(random.choice(greetings))
engine.runAndWait()

