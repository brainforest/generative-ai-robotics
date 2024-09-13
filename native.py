import speech_recognition as sr
  2 import openai
  3 import pyaudio
  4 
  5 # Initialize recognizer and OpenAI client
  6 recognizer = sr.Recognizer()
  7 client = openai.OpenAI()
  8 
  9 # Set the recording and audio playback parameters
 10 SAMPLE_RATE = 16000  # Valid argument for Microphone
 11 CHUNK = 1024
 12 HW_DEVICE_INDEX = 1  # Replace with the correct device index for HW:1,0
 13 
 14 # Initialize PyAudio for audio output
 15 p = pyaudio.PyAudio()
 16 
 17 # Function to perform speech-to-text and send to OpenAI GPT-4o-mini model
 18 def listen_and_speak():
 19     with sr.Microphone(sample_rate=SAMPLE_RATE) as source:  # No 'channels' argument
 20         print("Ortam gürültüsüne göre ayarlama yapılıyor... Lütfen bekleyin.")
 21         recognizer.adjust_for_ambient_noise(source)
 22 
 23         while True:
 24             print("Dinleniyor... (Çıkmak için CTRL + C)")
 25             try:
 26                 # Capture the audio from the microphone
 27                 audio_data = recognizer.listen(source)
 28 
 29                 # Perform speech-to-text in Turkish
 30                 text = recognizer.recognize_google(audio_data, language='tr-TR')
 31                 print("Dediğiniz: " + text)
 32 
 33                 # Prepate prompt
 34                 prompt = f"lütfen bilimsel kısa bir cevap ver {text}"
 35 
 36                 # Prepare the conversation history with recognized text
 37                 conversation_history = [{"role": "user", "content": prompt}]
 38 
 39                 # Send the recognized text to OpenAI GPT model
 40                 completion = client.chat.completions.create(
 41                     model="gpt-4o-mini",
 42                     messages=conversation_history,
 43                     temperature=1,
 44                     max_tokens=2048,
 45                     top_p=1,
 46                     frequency_penalty=0,
 47                     presence_penalty=0,
 48                     response_format={
 49                       "type": "text"
 50                     }
 51                 )
 52 
 53                 # Get the response from GPT
 54                 gpt_response = completion.choices[0].message.content
 55                 print("OpenAI Yanıtı: " + gpt_response)
 56 
 57                 # Now speak the response using OpenAI's text-to-speech
 58                 stream = p.open(format=pyaudio.paInt16,
 59                                 channels=1,
 60                                 rate=24000,
 61                                 output=True,
 62                                 output_device_index=HW_DEVICE_INDEX)  # Specify device index
 63 
 64                 # Create a TTS request and stream the response
 65                 with client.audio.speech.with_streaming_response.create(
 66                         model="tts-1",
 67                         voice="onyx",
 68                         input=gpt_response,
 69                         response_format="pcm") as tts_response:
 70 
 71                     # Stream the TTS response and play audio
 72                     for chunk in tts_response.iter_bytes(CHUNK):
 73                         stream.write(chunk)
 74 
 75                 # Close the stream after speaking
 76                 stream.stop_stream()
 77                 stream.close()
 78 
 79             except sr.UnknownValueError:
 80                 print("Ses anlaşılamadı.")
 81             except sr.RequestError as e:
 82                 print(f"Google Ses Tanıma servisine ulaşılamıyor; {e}")
 83             except Exception as e:
 84                 print(f"OpenAI API hatası: {e}")
 85 
 86 # Call the function to continuously listen, recognize speech, and speak the response
 87 try:
 88     listen_and_speak()
 89 except KeyboardInterrupt:
 90     print("\nDinleme durduruldu.")
 91 
 92 # Terminate PyAudio when done
 93 p.terminate()

