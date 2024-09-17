import time
import random
import numpy as np
from pathlib import Path
from openai import OpenAI
import pyaudio
from io import BytesIO
import re
from num2words import num2words

# Replace this with the correct device index for hw:1,0 from the previous step
device_index = 1  # Example index, replace with the actual index

# OpenAI istemcisi
client = OpenAI()

# Ses parametreleri
volume_factor = 3.0
p = pyaudio.PyAudio()

# Rastgele seçilecek cümleler listesi

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

