#!/usr/bin/env python3
"""
Generate sfx_victory.wav - ascending tone for successful completion.
Duration: ~0.30 seconds
Frequency sweep: 700 Hz → 950 Hz
Minimalist sine wave with gentle fade-out
"""

import wave
import math
import os

# Audio parameters
sample_rate = 44100  # Hz
duration = 0.30  # seconds
freq_start = 700  # Hz
freq_end = 950  # Hz
volume = 0.20  # (0-1 range)

# Generate samples
num_samples = int(sample_rate * duration)

samples = []

for i in range(num_samples):
    t = i / sample_rate
    progress = t / duration
    frequency = freq_start + (freq_end - freq_start) * progress
    value = math.sin(2 * math.pi * frequency * t)
    fade = math.exp(-5 * progress)
    value *= fade
    value *= volume
    samples.append(int(value * 32767))

# Write to WAV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "assets", "audio", "sfx_victory.wav")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with wave.open(output_path, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(b''.join(int(s).to_bytes(2, byteorder='little', signed=True) for s in samples))

print(f"Created {output_path}")
print(f"Duration: {duration}s, Frequency sweep: {freq_start}Hz → {freq_end}Hz, Volume: {volume}")
