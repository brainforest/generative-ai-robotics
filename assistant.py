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
import numpy as np

# alloy, echo, fable, onyx, nova, shimmer
voice = "nova"

# OpenAI interface
client = OpenAI()

# To speak louder
volume_factor = 3.0

# Rastgele seçilecek cümleler listesi
phrases = [
    "Haydi, bana bir soru sor! Bilim, uzay, matematik veya tarih hakkında merak ettiğin bir şey olabilir.",
    "Bugün hangi konuda konuşmak istersin? Teknoloji mi, doğa mı?",
    "Sana ilginç bir bilgi vereyim mi? Hangi konuda öğrenmek istersin?",
    "Matematik sorularına hazır mısın? Hadi bir soru sor!",
    "Uzayda yaşam hakkında ne düşünüyorsun? Merak ettiğin soruları bana sorabilirsin."
]


facts = [
    "Dünya'nın yer çekimi kuvveti, üzerindeki cisimleri merkeze doğru çeker.",
    "Bir atom, proton, nötron ve elektronlardan oluşur.",
    "Işık, elektromanyetik dalgalar olarak hareket eder.",
    "Hücre, tüm canlıların temel yapı taşıdır.",
    "Fotosentez, bitkilerin güneş ışığını kullanarak enerji üretme sürecidir.",
    "Newton'un üçüncü yasasına göre, her etkiye karşılık bir tepki vardır.",
    "Karbon elementinin atom numarası 6'dır.",
    "Dünya'nın manyetik alanı, güneş rüzgarlarına karşı koruma sağlar.",
    "İnsan beyni, yaklaşık 100 milyar sinir hücresinden oluşur.",
    "Bir madde, katı, sıvı ve gaz gibi üç ana halde bulunabilir.",
    "DNA, genetik bilgiyi taşıyan moleküldür.",
    "Einstein'ın görecelik teorisi, kütle ile uzay-zamanın nasıl etkileştiğini açıklar.",
    "Ozon tabakası, güneşin zararlı UV ışınlarına karşı koruma sağlar.",
    "Deniz suyu, %3.5 oranında tuz içerir.",
    "Bitkiler, karbondioksiti fotosentez yoluyla oksijene dönüştürür.",
    "Bir yıl, Dünya'nın Güneş etrafında bir tur atması ile ölçülür.",
    "Kara delikler, ışığın bile kaçamayacağı kadar güçlü çekim kuvvetine sahiptir.",
    "Bir elektron, atom çekirdeği etrafında negatif yüklü bir parçacıktır.",
    "Ay'ın yüzeyi, Dünya'daki okyanusların gelgitlerini etkiler.",
    "Sıcaklık, bir maddenin moleküler hareketinin bir ölçüsüdür.",
    "Doppler etkisi, bir dalganın frekansındaki değişikliktir.",
    "Hidrojeni yakmak, enerji üretmenin en verimli yollarından biridir.",
    "Bir güneş sistemi, bir yıldız ve onun etrafında dönen gezegenlerden oluşur.",
    "Bir protein, amino asitlerin uzun zincirlerinden oluşur.",
    "Hücre bölünmesi, canlıların büyümesini ve üremesini sağlar.",
    "Enerji, ne yaratılır ne yok edilir; sadece şekil değiştirir.",
    "Evrende milyarlarca galaksi vardır.",
    "Bir termit kolonisi, yüz binlerce bireyden oluşabilir.",
    "Gökkuşağı, ışığın su damlacıklarında kırılmasıyla oluşur.",
    "Yer kabuğu, çeşitli kaya türlerinden oluşur.",
    "Bir kara deliğin olay ufkunu aşan cisimler geri dönemez.",
    "Mars, Güneş Sistemi'ndeki dördüncü gezegendir.",
    "Plazma, bir maddenin en sıcak ve enerjik halidir.",
    "Bir yıldızın yaşam döngüsü, kütlesine bağlıdır.",
    "Einstein'ın E=mc² formülü, kütle ve enerjinin birbirine dönüştürülebileceğini açıklar.",
    "Ay, Dünya'nın doğal uydusudur.",
    "Beyin, merkezi sinir sisteminin en karmaşık organıdır.",
    "Radyo dalgaları, elektromanyetik spektrumun en uzun dalga boyuna sahiptir.",
    "Bir enzim, kimyasal reaksiyonları hızlandıran biyolojik bir katalizördür.",
    "Dinozorlar, 65 milyon yıl önce bir asteroid çarpması sonucu yok oldu.",
    "Bir kuşun kanat yapısı, aerodinamik prensiplerle uçmasını sağlar.",
    "Yağmur, atmosferdeki su buharının yoğunlaşmasıyla oluşur.",
    "Dünya'nın ekseni, eğik olduğu için mevsimler oluşur.",
    "Bir bitki tohumu, uygun koşullarda filizlenir.",
    "Bir elementin atom numarası, çekirdeğindeki proton sayısını gösterir.",
    "Bir molekül, iki ya da daha fazla atomun birleşmesiyle oluşur.",
    "Vücudumuzdaki kaslar, hareket etmek için enerji kullanır.",
    "Yerçekimi, uzaydaki her cismin birbirini çekmesine neden olur.",
    "Bir bakteriyel enfeksiyon, antibiyotiklerle tedavi edilebilir.",
    "Dünya atmosferi, %78 azot ve %21 oksijen içerir.",
    "Bir güneş patlaması, güneş yüzeyinde büyük enerji boşalmalarına neden olur.",
    "Dalgalar, enerji taşır ancak maddeyi taşımadan hareket eder.",
    "Karasal bitkiler, kökleri aracılığıyla suyu emer.",
    "Karbondioksit, sera etkisine katkıda bulunan bir gazdır.",
    "Volkanik patlamalar, Dünya'nın iç katmanlarından gelen basınçla oluşur.",
    "Dinozor fosilleri, Dünya'nın eski yaşam formlarına dair kanıtlar sağlar.",
    "Bir elektrik akımı, elektronların bir iletken üzerinden akışıyla oluşur.",
    "Deri, vücudumuzun en büyük organıdır.",
    "Kediler, düşük ışık koşullarında görme yeteneğine sahiptir.",
    "Venüs, Güneş Sistemi'ndeki en sıcak gezegendir.",
    "Kuantum mekaniği, atom altı parçacıkların davranışlarını inceleyen bir fizik dalıdır.",
    "Bir mıknatısın kuzey kutbu, diğer mıknatısların güney kutbu ile çekim kuvveti oluşturur.",
    "Arılar, bitkiler arasındaki polen taşıyıcılarıdır.",
    "Bir karınca kolonisi, işbirliği ile devasa yapılar inşa edebilir.",
    "Hücre zarları, hücre içine ve dışına madde taşınmasını kontrol eder.",
    "Karadelikler, devasa kütlelerin uzay-zamanı bükmesiyle oluşur.",
    "Bir bitki fotosentez sırasında oksijen üretir.",
    "Ay yüzeyi kraterlerle doludur.",
    "Bir balinanın sesi kilometrelerce öteden duyulabilir.",
    "Bir yıldızın çekirdeğinde nükleer füzyon gerçekleşir.",
    "Bir DNA molekülü çift sarmallı bir yapıya sahiptir.",
    "Elektronlar, negatif yüklü temel parçacıklardır.",
    "Fotonlar, ışığın temel enerji paketleridir.",
    "Bir güneş paneli, güneş ışığını elektrik enerjisine dönüştürür.",
    "Deprem, yer kabuğundaki fay hatlarının hareketi sonucu oluşur.",
    "Kuvvet, bir cismin hareketini değiştiren etkidir.",
    "Bir kimyasal reaksiyon, iki veya daha fazla maddenin birleşerek yeni maddeler oluşturmasıdır.",
    "Su, H₂O kimyasal formülüne sahiptir.",
    "Evrim, türlerin zamanla değişmesi sürecidir.",
    "Ay, Dünya etrafında yaklaşık 29,5 günde bir tur atar.",
    "Vücudumuzdaki hücreler, enerji üretmek için oksijen kullanır.",
    "Bir yıldırım, atmosferdeki elektriksel boşalmalarla oluşur.",
    "Kutup ışıkları, manyetik alanla etkileşen güneş rüzgarlarının sonucudur.",
    "Bir yıldızın parlaklığı, onun enerjisinin bir ölçüsüdür.",
    "Bir kara delik, evrendeki en yoğun nesnelerden biridir.",
    "Ses, hava moleküllerinin titreşimiyle iletilir.",
    "Teleskoplar, uzak gökcisimlerini incelemek için kullanılır.",
    "Bir sıcak hava balonu, sıcak havanın yükselme prensibine dayanır.",
    "Bir elmas, karbon atomlarının kristal yapısıyla oluşur.",
    "Dünya'nın atmosferi, uzaydaki radyasyona karşı bir koruma sağlar.",
    "Bir manyetik alan, hareket eden elektrik yükleri tarafından oluşturulur.",
    "Güneş, Dünya'dan 150 milyon kilometre uzaklıktadır.",
    "Hidrojen, evrendeki en bol elementtir.",
    "Bir kuasar, evrendeki en parlak nesnelerden biridir."
]

# Bu array 1000 cümle içeriyor.

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

question_headers = ["ilkokul seviyesinde kısa cevap ver: "] 

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
    return [{"role": "system", "content": "ilkokul seviyesinde kısa cevap ver: ."}]

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


def text_to_speech(phrase):
    """Belirtilen metni seslendir ve sesin hacmini artır."""
   
    pixels.speak()

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

    pixels.off()

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
    text_to_speech(answer)
    time.sleep(1)

    return " "

def _speak(speech_file_path):
    pixels.speak()
    # MP3 dosyasını mpg123 ile oynatın
    volume_factor = 164_000  # Adjust this value to change the volume 
    subprocess.run([ "mpg123", "-f", str(volume_factor), str(speech_file_path) ])
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

counter = 0

# Main loop
while True:
    if (button_pressed):
        question = _listen()
        if (len(question) > 3):
            answer = think_and_answer(question)
            time.sleep(1)
            counter = 0
    else:
        # Eğer 10 saniyede bir metin okunacaksa
        if counter == 15:
            selected_phrase = random.choice(facts)
            text_to_speech(selected_phrase)

        if counter >= 30:
            selected_phrase = random.choice(phrases)
            text_to_speech(selected_phrase)
            counter = 0
        else:
            counter += 1

    time.sleep(1)
