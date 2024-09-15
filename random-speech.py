import time
import random
import numpy as np
from pathlib import Path
from openai import OpenAI
import pyaudio

# OpenAI istemcisi
client = OpenAI()

# Ses parametreleri
volume_factor = 3.0
p = pyaudio.PyAudio()

# Rastgele seçilecek cümleler listesi
phrases = [
    "Haydi, bana bir soru sor! Bilim, uzay, matematik veya tarih hakkında merak ettiğin bir şey olabilir.",
    "Bugün hangi konuda konuşmak istersin? Teknoloji mi, doğa mı?",
    "Sana ilginç bir bilgi vereyim mi? Hangi konuda öğrenmek istersin?",
    "Matematik sorularına hazır mısın? Hadi bir soru sor!",
    "Uzayda yaşam hakkında ne düşünüyorsun? Merak ettiğin soruları bana sorabilirsin."
]

def text_to_speech(phrase, volume_factor):
    """Belirtilen metni seslendir ve sesin hacmini artır."""
    
    # OpenAI TTS API'si ile ses dosyasını oluştur ve ses akışı başlat
    stream = p.open(format=8, channels=1, rate=24_000, output=True)
    
    with client.audio.speech.with_streaming_response.create(
        model="tts-1-hd",
        voice="nova",
        input=phrase,
        response_format="pcm"
    ) as response:
        # Gelen ses verisini chunk chunk işle
        for chunk in response.iter_bytes(1024):
            # PCM verisini numpy dizisine çevir ve sesi yükselt
            audio_data = np.frombuffer(chunk, dtype=np.int16)
            audio_data = np.clip(audio_data * volume_factor, -32768, 32767).astype(np.int16)
            stream.write(audio_data.tobytes())
    
    stream.stop_stream()
    stream.close()

# Ana döngü
while True:
    # Rastgele bir cümle seç
    selected_phrase = random.choice(phrases)
    print(f"Seçilen cümle: {selected_phrase}")

    # Metni seslendir
    text_to_speech(selected_phrase, volume_factor)

    # 10 saniye bekle
    time.sleep(10)

