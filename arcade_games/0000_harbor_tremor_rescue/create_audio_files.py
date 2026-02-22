import wave
import struct
import os
import math

# Audio directory
audio_dir = os.path.join(os.path.dirname(__file__), 'assets', 'audio')

# Create simple sine wave data
amplitude = 32767 // 2
sample_rate = 22050

def create_wav(filename, freq=440, duration=0.5):
    filepath = os.path.join(audio_dir, filename)
    num_samples = int(sample_rate * duration)
    
    with wave.open(filepath, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        frames = []
        for i in range(num_samples):
            sample = int(amplitude * math.sin(2 * math.pi * freq * i / sample_rate))
            frames.append(struct.pack('<h', sample))
        
        wav_file.writeframes(b''.join(frames))
    print(f'Created {filename}')

# Create all audio files
create_wav('music_loop.wav', freq=440, duration=2.0)
create_wav('sfx_pickup.wav', freq=800, duration=0.1)
create_wav('sfx_drop.wav', freq=600, duration=0.15)
create_wav('sfx_hit.wav', freq=300, duration=0.2)
create_wav('sfx_sail.wav', freq=900, duration=0.3)
create_wav('sfx_depart.wav', freq=700, duration=0.25)
create_wav('sfx_defeat.wav', freq=200, duration=0.5)

print('All audio files created successfully in ' + audio_dir)
