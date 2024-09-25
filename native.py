import speech_recognition as sr
import openai
import pyaudio
 
# Initialize recognizer and OpenAI client
recognizer = sr.Recognizer()
client = openai.OpenAI()

voice="nova"

# Set the recording and audio playback parameters
SAMPLE_RATE = 16000  # Valid argument for Microphone
CHUNK = 1024
HW_DEVICE_INDEX = 1  # Replace with the correct device index for HW:1,0

# Initialize PyAudio for audio output
p = pyaudio.PyAudio()

# Function to perform speech-to-text and send to OpenAI GPT-4o-mini model
def listen_and_speak():
    with sr.Microphone(sample_rate=SAMPLE_RATE) as source:  # No 'channels' argument
        print("Ortam gürültüsüne göre ayarlama yapılıyor... Lütfen bekleyin.")
        recognizer.adjust_for_ambient_noise(source)

        while True:
            print("Dinleniyor... (Çıkmak için CTRL + C)")
            try:
                # Capture the audio from the microphone
                audio_data = recognizer.listen(source)

                # Perform speech-to-text in Turkish
                text = recognizer.recognize_google(audio_data, language='tr-TR')
                print("Dediğiniz: " + text)

                # Prepate prompt
                prompt = f"lütfen bilimsel kısa bir cevap ver {text}"

                # Prepare the conversation history with recognized text
                conversation_history = [{"role": "user", "content": prompt}]

                # Send the recognized text to OpenAI GPT model
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=conversation_history,
                    temperature=1,
                    max_tokens=2048,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    response_format={
                      "type": "text"
                    }
                )

                # Get the response from GPT
                gpt_response = completion.choices[0].message.content
                print("OpenAI Yanıtı: " + gpt_response)

                # Now speak the response using OpenAI's text-to-speech
                stream = p.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=24000,
                                output=True,
                                output_device_index=HW_DEVICE_INDEX)  # Specify device index

                # Create a TTS request and stream the response
                with client.audio.speech.with_streaming_response.create(
                        model="tts-1",
                        voice=voice,
                        input=gpt_response,
                        response_format="pcm") as tts_response:

                    # Stream the TTS response and play audio
                    for chunk in tts_response.iter_bytes(CHUNK):
                        stream.write(chunk)

                # Close the stream after speaking
                stream.stop_stream()
                stream.close()

            except sr.UnknownValueError:
                print("Ses anlaşılamadı.")
            except sr.RequestError as e:
                print(f"Google Ses Tanıma servisine ulaşılamıyor; {e}")
            except Exception as e:
                print(f"OpenAI API hatası: {e}")

# Call the function to continuously listen, recognize speech, and speak the response
try:
    listen_and_speak()
except KeyboardInterrupt:
    print("\nDinleme durduruldu.")

# Terminate PyAudio when done
p.terminate()
