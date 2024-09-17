import time
import random
import numpy as np
from pathlib import Path
from openai import OpenAI
import pyaudio
from io import BytesIO
import re
from num2words import num2words
from scientific_facts import facts

# Replace this with the correct device index for hw:1,0 from the previous step
device_index = 1  # Example index, replace with the actual index

# OpenAI istemcisi
client = OpenAI()

# Ses parametreleri
volume_factor = 3.0
p = pyaudio.PyAudio()

def convert_numbers_to_words(text):
    """Convert percentages like 3.5 or 90 to their Turkish equivalents."""
    
    # Regular expression to find percentages like %3.5 or %90
    percentage_pattern = re.compile(r'(\d+(\.\d+)?)')
    
    def replace_with_words(match):
        number = match.group(1)
        # Convert the number to Turkish words
        if '.' in number:
            # Handle decimal numbers
            parts = number.split('.')
            integer_part = num2words(int(parts[0]), lang='tr')
            decimal_part = num2words(int(parts[1]), lang='tr')
            return f"{integer_part} virgül {decimal_part}"
        else:
            # Handle whole numbers
            return f"{num2words(int(number), lang='tr')}"
    
    # Replace all percentages in the text with their Turkish equivalents
    return percentage_pattern.sub(replace_with_words, text)


def adjust_volume(audio_data, volume_factor,sample_width) :

    """Adjusts the volume of PCM audio data.

    Args:
        audio_data (bytes): Raw PCM audio data.
        volume_factor (float): Factor by which to increase the volume.
        sample_width (int): The width of each sample in bytes.

    Returns:
        bytes: Adjusted PCM audio data.
    """
    # Convert binary data to numpy array for processing
    dtype = np.int16 if sample_width == 2 else np.int8
    audio_array = np.frombuffer(audio_data, dtype=dtype)

    # Apply volume adjustment
    audio_array = np.clip(audio_array * volume_factor, -32768, 32767)

    # Convert numpy array back to binary data
    adjusted_audio_data = audio_array.astype(np.int16).tobytes()

    return adjusted_audio_data

def play_audio_in_chunks():
    """Plays raw PCM audio from a file in chunks using PyAudio stream."""

    file_path = Path(__file__).parent / "speech.pcm"  # Assuming this file contains raw PCM data

    # Define audio parameters for PCM (adjust these values based on your PCM file specifications)
    channels = 1         # Mono audio
    sample_rate = 24000   # 24 kHz sample rate
    sample_width = 2      # 16-bit audio (2 bytes per sample)
    
    # Open stream with the specified PCM format
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=sample_rate,
                    output=True,
                    output_device_index=device_index)

    # Read the PCM file in binary mode and play it in chunks
    chunk_size = 4096  # Adjust chunk size if needed
    with open(file_path, 'rb') as pcm_file:
        audio_data = pcm_file.read(chunk_size)

        while len(audio_data) > 0:
            # Play the chunk of PCM data
            stream.write(adjust_volume(audio_data, volume_factor, sample_width))
            # Read the next chunk
            audio_data = pcm_file.read(chunk_size)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()


# Write into file .
def text_to_file(phrase):
    """Writes the generated PCM audio to a file."""
    
    speech_file_path = Path(__file__).parent / "speech.pcm"

    # Open the file in write-binary mode to store PCM data
    with open(speech_file_path, "wb") as f:
        # Start the streaming response
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=phrase,
            response_format="pcm"
        ) as response:
            # Write chunks of audio data to the file
            for chunk in response.iter_bytes(1024):
                f.write(chunk)

# Real-time text-to-speech 
def text_to_speech(phrase):
    """Belirtilen metni seslendir ve sesin hacmini artır."""

    # OpenAI TTS API'si ile ses dosyasını oluştur ve ses akışı başlat
    stream = p.open(format=8, channels=1, rate=24_000, output=True,output_device_index=device_index)

    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="nova",
        input=phrase,
        response_format="pcm"
    ) as response:
        # Gelen ses verisini chunk chunk işle
        for chunk in response.iter_bytes(1024):
            stream.write(chunk)

    stream.stop_stream()
    stream.close()

# Ana döngü
while True:
    # Rastgele bir cümle seç
    selected_phrase = random.choice(facts)

    # do some changes
    selected_phrase = convert_numbers_to_words(selected_phrase)
    print(f"Seçilen cümle: {selected_phrase}")

    # Metni seslendir
    #text_to_speech(selected_phrase)
    text_to_file(selected_phrase)
    play_audio_in_chunks()


    # 10 saniye bekle
    time.sleep(10)

