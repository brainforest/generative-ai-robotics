import time
import random
import pyaudio
from google.cloud import texttospeech
from google.oauth2 import service_account

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
    "Bir kuasar, evrendeki en parlak nesnelerden biridir.",
    "Su, dünyanın yüzeyinin yaklaşık %71'ini kaplar.",
    "İnsan vücudundaki en büyük organ deridir.",
    "Güneş sistemi, yaklaşık 4.6 milyar yıl önce oluştu.",
    "Dünya'nın çekirdeği demir ve nikelden oluşur.",
    "Uzayda ses yayılmaz çünkü ses, bir ortamda titreşen moleküllere ihtiyaç duyar.",
    "Bir ışık yılı, ışığın bir yılda kat ettiği mesafedir, yaklaşık 9.46 trilyon kilometre.",
    "Yıldızlar, nükleer füzyon yoluyla enerji üretir.",
    "Sıvı azot, -196°C'de kaynar.",
    "İnsan beyni yaklaşık 86 milyar nöron içerir.",
    "Karadelikler, çekim kuvvetleri o kadar güçlüdür ki, ışık bile kaçamaz.",
    "Venüs gezegeni, Güneş Sistemi'ndeki en sıcak gezegendir.",
    "Bir insan gözünde yaklaşık 120 milyon çubuk hücresi ve 6 milyon koni hücresi vardır.",
    "Dünya'nın en derin noktası Mariana Çukuru'dur, yaklaşık 11,000 metre derinliktedir.",
    "Zeytin ağaçları, 1,000 yıldan fazla yaşayabilir.",
    "Bir yıldızın rengini, sıcaklığı belirler. Mavi yıldızlar en sıcak, kırmızı yıldızlar ise en soğuktur.",
    "Elektronlar, atom çekirdeğinin etrafında döner ve negatif yük taşır.",
    "Ay, Dünya'nın etrafında yaklaşık 27.3 günde bir döner.",
    "Kimi böcekler, vücutlarının %90'ından fazlasını su olarak içerir.",
    "Örümcekler, kendi ağılarını örerken sıvı protein üretirler.",
    "Atmosferimizdeki en fazla gaz azottur, yaklaşık %78.",
    "Işık, boşlukta saatte yaklaşık 300,000 kilometre hızla hareket eder.",
    "Yeryüzündeki en yüksek dağ Everest'tir, 8,848 metre yüksekliğindedir.",
    "Karanlık madde, evrenin kütlesinin yaklaşık %27'sini oluşturur, ama doğrudan gözlemlenemez.",
    "DNA, tüm canlıların genetik talimatlarını içerir ve bir hücrede yaklaşık 2 metre uzunluğundadır.",
    "Dünya'nın çekirdeği, yüzeyin altındaki katmanlardan yaklaşık 2,900 kilometre derindedir.",
    "Karıncalar, kendi ağırlıklarının 50 katı kadar ağırlık taşıyabilir.",
    "Jüpiter, Güneş Sistemi'ndeki en büyük gezegendir.",
    "Denizanası, genellikle %95 su içerir.",
    "İnsanlar, 5 farklı tat alabilir: tatlı, ekşi, acı, tuzlu ve umami.",
    "Gözbebeği, ışığın gözümüze giriş miktarını kontrol eder.",
    "Hava kirliliği, solunum yolu hastalıklarına ve kalp rahatsızlıklarına neden olabilir.",
    "Dünya'daki en hızlı hayvan, çita'dır ve saatte 100 kilometreye kadar hızlanabilir.",
    "Yüksek sesler, işitme kaybına yol açabilir.",
    "Bir elma, yaklaşık 80% su içerir.",
    "Güneş, her saniye yaklaşık 4.1 milyon ton maddeyi enerjiye dönüştürür.",
    "Mavi balina, dünyadaki en büyük hayvandır.",
    "Sıcaklık düştüğünde, bazı metaller büzülürken bazıları genişleyebilir.",
    "Dünya'nın yüzeyinde toplam 5 okyanus vardır: Pasifik, Atlantik, Hint, Güney ve Arktik.",
    "Şeker, beynin ödül merkezini aktive eder ve mutluluk hissi yaratabilir.",
    "Gökyüzünün rengi, atmosferdeki moleküllerin ve parçacıkların ışığı saçması nedeniyle mavi görünür.",
    "Karanlık enerji, evrenin hızlanarak genişlemesini sağlayan bilinmeyen bir güçtür.",
    "Uzaydaki sıcaklık, -270°C'ye kadar düşebilir.",
    "Şekerleme, beynin dopamin salgılamasına neden olabilir.",
    "Titan, Satürn'ün en büyük uydusudur ve Dünya'dan büyük bir atmosferi vardır.",
    "Işık, suyun içinden geçerken kırılır ve farklı hızlarla hareket eder.",
    "Düşük sıcaklıklar, bazı sıvıları donmaya neden olabilir.",
    "İnsanlar, yaşlandıkça beyin hücrelerini kaybedebilir.",
    "Güneş'in dış tabakası korona, iç tabakası ise fotosfer olarak adlandırılır.",
    "Su, sıvı, katı ve gaz formunda bulunabilir.",
    "Zeytinler, antioksidanlar ve sağlıklı yağlar açısından zengindir.",
    "Ay'ın yüzeyi, kraterlerle kaplıdır çünkü atmosferi yoktur.",
    "Hava durumu tahminleri, meteorolojik verilere ve modellerine dayanır.",
    "Tıbbi araştırmalar, hastalıkları ve tedavi yöntemlerini geliştirmek için yapılır.",
    "DNA, her bireyin genetik bilgisini taşır ve kalıtım yoluyla aktarılır.",
    "Küresel ısınma, gezegenin ortalama sıcaklığının artmasına neden olabilir.",
    "Çiçekler, polinatörler tarafından tozlaşır ve üremeyi sağlar.",
    "İnsan vücudu, toplamda yaklaşık 37.2°C sıcaklıkta tutulur.",
    "Su, hidrojen ve oksijen atomlarından oluşur.",
    "Elektrik akımı, bir iletken boyunca hareket eden elektronların akışıdır.",
    "Dünya'nın manyetik alanı, kuzey ve güney kutuplarını belirler.",
    "Bilimsel yöntemde, hipotezler test edilir ve sonuçlar değerlendirilir.",
    "Kuantum mekaniği, atom altı parçacıkların davranışlarını inceler.",
    "Kısırlık tedavileri, çiftlerin çocuk sahibi olabilmesi için çeşitli yöntemler sunar.",
    "Sıcaklık, bir maddeyi katı, sıvı veya gaz hale getirebilir.",
    "Kutup yıldızları, kuzey ve güney yarımkürede farklı yönleri gösterir.",
    "Mikroskobik organizmalar, ekosistemlerin temel parçalarını oluşturur.",
    "Su, insanların yaşamsal ihtiyaçlarından biridir ve vücut ağırlığının yaklaşık %60'ını oluşturur.",
    "Yerçekimi, tüm cisimleri Dünya'ya çeker.",
    "Kritik sıcaklık, bir maddenin sıvıdan gaz haline geçiş yaptığı noktadır.",
    "Mikroplar, birçok hastalığın nedenidir ve hijyenik koşullar altında kontrol edilebilirler.",
    "Birçok bitki, fotosentez yoluyla ışığı enerjiye dönüştürür.",
    "İnsanlar, yaklaşık 20,000-30,000 koku alıcıya sahiptir.",
    "Birçok yıldız, kendisinden çok daha büyük olan gezegenlere sahip olabilir.",
    "Güneş, çekirdeğinde her saniye 600 milyon ton hidrojen yakar.",
    "Denizler, gezegenin en büyük su rezervuarlarını içerir.",
    "Gözler, renkleri algılamak için ışığı farklı dalga boylarına ayırır.",
    "Işık hızının ötesinde hareket eden parçacıklar, henüz gözlemlenmemiştir.",
    "Biyolojik çeşitlilik, ekosistemlerin sağlıklı kalmasını sağlar.",
    "Yıldırım, elektrik yüklerinin havadaki boşalmasıdır ve genellikle bir bulut ile yer arasındaki ilişkiyle meydana gelir.",
    "Güneş sistemi, bir yıldız ve onun etrafında dönen gezegenler ve diğer gök cisimlerinden oluşur.",
    "Rüzgar, hava basıncındaki farklılıklar nedeniyle oluşur.",
    "Gözlerin rengi, iris adı verilen pigmentlere bağlıdır.",
    "Bazı deniz canlıları, ışık üretme yeteneğine sahiptir.",
    "Vücudumuzda bulunan bakteriler, sindirim sistemimizin sağlığı için önemlidir.",
    "Çözücüler, diğer maddelerin çözülmesini sağlayan sıvılardır.",
    "Güneş enerjisi, yenilenebilir bir enerji kaynağıdır ve çevre dostudur.",
    "Büyük patlama teorisi, evrenin başlangıcını açıklayan bir modeldir.",
    "Dışkı, sindirilmiş yiyeceklerin ve atıkların vücuttan atılmasıdır.",
    "Tuzlu su, tatlı sudan daha yoğundur ve daha fazla kaldırma gücüne sahiptir.",
    "Bazı canlılar, değişen çevre koşullarına uyum sağlamak için renk değiştirebilir.",
    "Gözlükler, gözleri düzeltmek veya korumak için kullanılır.",
    "Sıcaklık artışı, deniz seviyesinin yükselmesine neden olabilir.",
    "Kuvvet, bir nesnenin hareketini değiştiren bir etkidir.",
    "Elektromıknatıs, elektrik akımı ile manyetik özellik kazanan bir malzemedir.",
    "Güneş'in çekim gücü, gezegenleri yörüngelerinde tutar.",
    "Kara delikler, büyük bir çekim gücüne sahip olan ve etrafındaki her şeyi içine çeken gök cisimleridir.",
    "Bazı böcekler, savunma mekanizması olarak kimyasal madde salgılar.",
    "Yıldızlar, gaz ve toz bulutlarından oluşan dev bulutlarda doğar.",
    "Güneş ışığının yaklaşık %30'u Dünya'ya ulaşmadan atmosferde dağılır.",
    "Kuşlar, uçarak enerji tasarrufu yapabilirler.",
    "Havada bulunan su buharı, bulutların oluşmasına neden olabilir.",
    "Bazı bitkiler, kökleriyle suyu toplayarak çevresindeki toprağı besler.",
    "Birçok hayvan, savunma amaçlı renk değiştirme yeteneğine sahiptir.",
    "Mikroskoplar, çok küçük nesneleri incelemek için kullanılır.",
    "Büyük dinozorlar, milyonlarca yıl önce Dünya'da yaşamışlardır.",
    "Deniz suyu, tatlı suya göre daha yüksek bir tuzluluk oranına sahiptir.",
    "Birçok bitki, köklerinde depolanan suyu uzun süre saklayabilir.",
    "İnsan vücudu, her gün yaklaşık 1-2 litre su kaybeder.",
    "Bitkiler, fotosentez sırasında oksijen üretir.",
    "Gözler, çevresel ışığı algılamak için özel hücrelere sahiptir.",
    "Bazı mantarlar, ilaç üretimi için kullanılan önemli bileşenler içerir.",
    "Kutup bölgelerindeki sıcaklıklar, ekvator bölgelerine göre çok daha düşük olabilir.",
    "Dünyadaki en yüksek sıcaklık, Çöl bölgelerinde ölçülmüştür.",
    "Denizaltı volkanları, okyanus tabanında bulunan aktif volkanlardır.",
    "Meteorlar, uzaydan Dünya'ya doğru hareket eden küçük taşlardır.",
    "Karbondioksit, sera gazlarından biridir ve iklim değişikliğine neden olabilir.",
    "Dünya'nın atmosferi, çeşitli gazları içerir ve yaşamın devamını sağlar.",
    "Büyük patlama teorisi, evrenin genişlemekte olduğunu belirtir.",
    "Bazı organizmalar, kendilerini yenileyebilme yeteneğine sahiptir.",
    "Bazı mikroorganizmalar, toprak sağlığını artırabilir.",
    "Radyasyon, enerjinin çeşitli biçimlerinin yayılmasını ifade eder.",
    "Ay'ın yüzeyi, kraterler ve dağlar ile kaplıdır.",
    "Güneş'in iç sıcaklığı yaklaşık 15 milyon derece Celsius'tur.",
    "Şeker, enerji kaynağı olarak kullanılan bir karbonhidrat türüdür.",
    "Çiçekler, üreme sürecinde polinatörleri çeker.",
    "Yıldızlar, yüksek sıcaklık ve basınç altında enerji üretir.",
    "Birçok organizma, çevresel streslere dayanabilme yeteneğine sahiptir.",
    "Küçük gök cisimleri, gezegenlerin yüzeylerine çarpabilir.",
    "Denizlerin derinlikleri, çeşitli yaşam formlarını barındırır.",
    "Bazı canlılar, karanlıkta parlayabilir.",
    "Birçok organizma, ışığa duyarlıdır ve çevresine göre tepki verebilir.",
    "Sıvı kristaller, hem sıvı hem de katı özelliklere sahip özel materyallerdir.",
    "Gözler, renkleri algılamak için farklı fotoreseptörler içerir.",
    "Bazı dinozorlar, uzun kuyruklarıyla savunma yapabilirdi.",
    "Denizler, dünyanın iklimini etkileyen büyük su kütleleridir.",
    "Güneş ışığı, Dünya'nın iklimini etkileyen önemli bir faktördür.",
    "Küresel ısınma, buzulların erimesine neden olabilir.",
    "Bazı bitkiler, çevresel koşullara göre hızlı bir şekilde büyüyebilir.",
    "Büyük gök cisimleri, gezegenler ve yıldızlar arasındaki boşluklarda bulunur.",
    "Denizler, okyanus akıntıları ile dünya genelinde enerji taşıyabilir.",
    "Küresel sıcaklıklar, insan faaliyetleriyle etkilenebilir."
]

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

