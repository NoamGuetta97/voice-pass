"""
This is the code suppose to run on the Sender side
"""


import json
import numpy as np
from scipy.io.wavfile import write
import pyaudio

def json_to_binary(json_data):
    json_string = json.dumps(json_data)
    binary_string = ''.join(format(ord(char), '08b') for char in json_string)
    return binary_string

def encode_data(data, sample_rate=44100, duration=0.1):  # Reduced duration for faster transfer
    frequencies = {'0': 1000, '1': 1500}
    encoded_signal = np.array([], dtype=np.float32)
    
    for bit in data:
        freq = frequencies[bit]
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        signal = 0.5 * np.sin(2 * np.pi * freq * t)
        encoded_signal = np.concatenate((encoded_signal, signal))
    
    return encoded_signal

def play_sound(encoded_signal, sample_rate=44100):
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=sample_rate,
                    output=True)
    
    stream.write(encoded_signal.tobytes())
    stream.stop_stream()
    stream.close()
    p.terminate()

json_data = {"name": "Alice", "age": 30, "city": "New York"}
binary_data = json_to_binary(json_data)
print(f"Binary data: {binary_data}")  # Debugging line to check binary conversion
encoded_signal = encode_data(binary_data)
print(f"Encoded signal length: {len(encoded_signal)}")  # Debugging line to check signal length
play_sound(encoded_signal)
