import pyaudio
import speech_recognition as sr
import pyttsx3
import random

# Initialize recognizer and text-to-speech engine
engine = pyttsx3.init()

# Greetings to choose from
greetings = ["Hello, how can I assist you?", "Hi there! What do you need?", "Hey! How can I help you?","Yes, master I listen you"]

# Get the current speech rate
current_rate = engine.getProperty('rate')
print(f"Current speech rate: {current_rate}")

# Set the speech rate to a slower value
slow_rate = current_rate - 100  # Decrease by 50, you can adjust this value
engine.setProperty('rate', slow_rate)

engine.say(random.choice(greetings))
engine.runAndWait()

engine.say("A black hole is a region of spacetime where gravity is so strong that nothing, not even light and other electromagnetic waves, is capable of possessing enough energy to escape it. Einstein's theory of general relativity predicts that a sufficiently compact mass can deform spacetime to form a black hole.")
engine.runAndWait()
