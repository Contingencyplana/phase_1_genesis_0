#!/usr/bin/env python3
"""
Generate sfx_spell_pickup.wav - a short pure-tone shimmer for crate pickup.
Duration: ~0.12 seconds
Frequency: 900 Hz
Gentle fade-out with low volume
"""

import numpy as np
import wave
import os

# Audio parameters
sample_rate = 44100  # Hz
duration = 0.12  # seconds
frequency = 900  # Hz
volume = 0.15  # low volume (0-1 range)

# Generate samples
num_samples = int(sample_rate * duration)
t = np.linspace(0, duration, num_samples, False)

# Pure 900 Hz sine wave
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
output_path = os.path.join(BASE_DIR, "assets", "audio", "sfx_spell_pickup.wav")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with wave.open(output_path, 'wb') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(waveform_int16.tobytes())

print(f"Created {output_path}")
print(f"Duration: {duration}s, Frequency: {frequency}Hz, Volume: {volume}")
