"""
This code suppost to run the reciever side
"""

import pyaudio
import numpy as np
import json

def record_sound(duration=3, sample_rate=44100):
    p = pyaudio.PyAudio()
    
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=1024)
    
    frames = []
    
    for _ in range(0, int(sample_rate / 1024 * duration)):
        data = stream.read(1024)
        frames.append(np.frombuffer(data, dtype=np.int16))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return np.concatenate(frames)

def decode_data(signal, sample_rate=44100, duration=0.1):  # Reduced duration for faster transfer
    frequencies = {1000: '0', 1500: '1'}
    decoded_data = ''
    samples_per_bit = int(sample_rate * duration)
    
    for i in range(0, len(signal), samples_per_bit):
        chunk = signal[i:i+samples_per_bit]
        freqs, psd = np.fft.rfftfreq(len(chunk), 1/sample_rate), np.abs(np.fft.rfft(chunk))
        peak_freq = freqs[np.argmax(psd)]
        bit = frequencies.get(int(round(peak_freq)), '')
        decoded_data += bit
        print(f"Chunk {i//samples_per_bit}: Peak frequency = {peak_freq}, Bit = {bit}")  # Debugging line
    
    return decoded_data

def binary_to_json(binary_data):
    try:
        if not binary_data:
            raise ValueError("Binary data is empty")
        
        json_string = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
        json_data = json.loads(json_string)
        return json_data
    except Exception as e:
        print(f"Error decoding JSON: {e}")
        print(f"Binary data: {binary_data}")
        return None

def continuous_receiver():
    while True:
        print("Recording sound...")
        recorded_signal = record_sound()
        print("Decoding data...")
        decoded_binary_data = decode_data(recorded_signal)
        print(f"Decoded binary data: {decoded_binary_data}")
        
        if decoded_binary_data:
            json_data = binary_to_json(decoded_binary_data)
            print(f"Decoded JSON data: {json_data}")
        else:
            print("No valid data received.")

continuous_receiver()
