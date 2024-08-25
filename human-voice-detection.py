import pyaudio
import webrtcvad

# Ayarlar
RESPEAKER_RATE = 16000  # Örnekleme hızı
RESPEAKER_CHANNELS = 1  # Kanal sayısı (VAD için mono gerekir)
RESPEAKER_WIDTH = 2  # Örnek genişliği (byte)
RESPEAKER_INDEX = 1  # Giriş cihazı ID'si
CHUNK_DURATION_MS = 30  # Veri blok süresi (milisaniye)
CHUNK = int(RESPEAKER_RATE * CHUNK_DURATION_MS / 1000)  # Veri blok boyutu
RECORD_SECONDS = 10  # Maksimum kayıt süresi

p = pyaudio.PyAudio()

# Ses girişi için stream aç
stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    input_device_index=RESPEAKER_INDEX
)

vad = webrtcvad.Vad()
vad.set_mode(3)  # 0 (çok agresif değil) - 3 (çok agresif) arasında VAD hassasiyeti

print("* recording")

frames = []

# Ses kaydını başlat
for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

    # VAD ile insan sesini kontrol et
    is_speech = vad.is_speech(data, RESPEAKER_RATE)
    
    if is_speech:
        print("Speech detected")
    else:
        print("Silence")

print("* done recording")

# Stream'i durdur ve kapat
stream.stop_stream()
stream.close()
p.terminate()

# Kayıt işlemi sonlandırıldı, `frames` liste halinde kaydedilmiş ses verisini içerir.

