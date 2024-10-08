from pathlib import Path
from openai import OpenAI

import subprocess


client = OpenAI()

# Ses dosyasının yolunu belirtin
speech_file_path = Path(__file__).parent / "speech.mp3"

# OpenAI TTS API'si ile ses dosyasını oluşturun
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",
    input="Haydi, bana bir soru sor! bilim, uzay, matematik veya tarih hakkında merak birşey olabilir." 
)

# Ses dosyasını dosyaya yazın
response.stream_to_file(speech_file_path)

# MP3 dosyasını mpg123 ile oynatın
subprocess.run([ "mpg123", str(speech_file_path)])

