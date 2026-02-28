#!/usr/bin/env python3
"""
Generate sfx_load_soft.wav - a soft low-frequency tone for successful cargo load.
Duration: ~0.08 seconds
Frequency: 450 Hz
Very low volume with gentle fade-out
No shimmer - plain sine wave
"""

import numpy as np
import wave
import os

# Audio parameters
sample_rate = 44100  # Hz
duration = 0.08  # seconds
frequency = 450  # Hz
volume = 0.10  # very low volume (0-1 range)

# Generate samples
num_samples = int(sample_rate * duration)
t = np.linspace(0, duration, num_samples, False)

# Plain 450 Hz sine wave (no shimmer)
waveform = np.sin(2 * np.pi * frequency * t)

# Gentle fade-out (exponential decay)
fade_out = np.exp(-5 * t / duration)
waveform = waveform * fade_out

# Apply volume
waveform = waveform * volume

# Convert to 16-bit PCM
waveform_int16 = np.int16(waveform * 32767)

# Write to WAV file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "assets", "audio", "sfx_load_soft.wav")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with wave.open(output_path, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(waveform_int16.tobytes())

print(f"Created {output_path}")
print(f"Duration: {duration}s, Frequency: {frequency}Hz, Volume: {volume}")
