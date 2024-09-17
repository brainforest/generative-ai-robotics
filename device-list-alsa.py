import pyaudio

p = pyaudio.PyAudio()

# List all audio devices
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    print(f"Device {i}: {device_info['name']}")

