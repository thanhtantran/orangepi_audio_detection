import sounddevice as sd
import numpy as np

# Define the input device based on the information you have
input_device = 'hw:2,0'  # Replace with the appropriate device name or identifier

# Other audio parameters
FORMAT = 'int16'  # Audio format (adjust as needed)
CHANNELS = 1  # Mono or 2 for stereo
RATE = 44100  # Sample rate (adjust as needed)
CHUNK = 1024  # Number of frames per buffer
THRESHOLD = 75 # 75 Bagus # 100 Aman banget # Adjust this value based on your setup

# Variable to keep track of audio detection
audio_detected = 0

# Configure the audio stream using the specified input device
stream = sd.InputStream(
    device=input_device,
    channels=CHANNELS,
    samplerate=RATE,
    dtype=FORMAT
)

with stream:
    print("Listening for audio from the specified input device... Press Ctrl+C to exit.")
    while True:
        # Read audio data from the input stream
        indata_raw, overflowed = stream.read(CHUNK)
        
        # Data diolah (dirata-rata)
        indata = np.abs(indata_raw).mean()

        # Check if audio data is present (adjust this threshold as needed)
        if indata > THRESHOLD:
            audio_detected = 1
        else:
            audio_detected = 0
        
        
        # Process the audio data as needed
        # You can add your audio processing logic here

        # You can print or use audio_detected as needed
        print(f"Audio Detected: {audio_detected}, indata_raw: {indata}")
