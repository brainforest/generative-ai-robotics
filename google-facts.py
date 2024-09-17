import time
import random
import pyaudio
from google.cloud import texttospeech
from google.oauth2 import service_account
from scientific_facts import facts

# Example index, replace with the actual index
device_index = 1 

# Set up credentials
credentials = service_account.Credentials.from_service_account_file('text-to-speech-raspberry-pi.json')
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Initialize PyAudio
p = pyaudio.PyAudio()

def text_to_speech(text):

    input_text = texttospeech.SynthesisInput(text=text)
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams( language_code="tr-TR", name="tr-TR-Standard-E")

    # Set up the audio config for LINEAR16 (raw PCM)
    audio_config = texttospeech.AudioConfig( audio_encoding=texttospeech.AudioEncoding.LINEAR16, speaking_rate=1)
    
    # Request the synthesis
    response = client.synthesize_speech( request={"input": input_text, "voice": voice, "audio_config": audio_config})

    # Open a stream to play the audio
    stream = p.open(format=pyaudio.paInt16,  # LINEAR16 is 16-bit audio
                    channels=1,  # Mono audio
                    rate=24000,  # Set the sample rate to 24kHz
                    output=True,
                    output_device_index=device_index)  # Set the output device

    # Stream the audio content from the response
    stream.write(response.audio_content)

    # Clean up the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()

# Ana döngü
while True:
    # Rastgele bir cümle seç
    selected_phrase = random.choice(facts)

    # do some changes
    print(f"Seçilen cümle: {selected_phrase}")

    # Metni seslendir
    #text_to_speech(selected_phrase)
    text_to_speech(selected_phrase)

    # 10 saniye bekle
    time.sleep(10)

