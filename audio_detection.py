import sounddevice as sd
import numpy as np
import time

# Audio configuration parameters
FORMAT = 'int16'
CHANNELS = 1
RATE = 44100
CHUNK = 1024
THRESHOLD = 75  # Initial threshold, will be calibrated

# Variables for detection
audio_detected = 0
window_size = 10
audio_levels = [0] * window_size
debounce_count = 0
debounce_threshold = 3

# Function to list available audio devices
def list_devices():
    print("Available audio devices:")
    print(sd.query_devices())

# Try to find the appropriate input device
try:
    list_devices()
    input_device = 'hw:2,0'  # Default, but you should select the correct one
    
    # Configure the audio stream
    stream = sd.InputStream(
        device=input_device,
        channels=CHANNELS,
        samplerate=RATE,
        dtype=FORMAT
    )
    
    # Calibration phase
    print("Calibrating ambient noise levels...")
    ambient_samples = []
    with stream:
        for _ in range(100):
            indata_raw, _ = stream.read(CHUNK)
            ambient_samples.append(np.abs(indata_raw).mean())
            time.sleep(0.01)
    
    ambient_level = sum(ambient_samples) / len(ambient_samples)
    THRESHOLD = ambient_level * 1.5  # Set threshold 50% above ambient
    print(f"Ambient noise level: {ambient_level:.2f}, Threshold set to: {THRESHOLD:.2f}")
    
    # Main detection loop
    with stream:
        print("Listening for audio... Press Ctrl+C to exit.")
        while True:
            try:
                # Read audio data from the input stream
                indata_raw, overflowed = stream.read(CHUNK)
                
                # Process the audio data (calculate average amplitude)
                current_level = np.abs(indata_raw).mean()
                
                # Use rolling average for smoother detection
                audio_levels.pop(0)
                audio_levels.append(current_level)
                average_level = sum(audio_levels) / window_size
                
                # Apply debounce mechanism to prevent rapid toggling
                if average_level > THRESHOLD:
                    debounce_count += 1
                    if debounce_count >= debounce_threshold:
                        audio_detected = 1
                else:
                    debounce_count = 0
                    if audio_detected == 1:
                        audio_detected = 0
                
                # Print detection status
                print(f"Audio Detected: {audio_detected}, Level: {average_level:.2f}, Threshold: {THRESHOLD:.2f}")
                
                # Add a small delay to reduce CPU usage
                time.sleep(0.01)
                
            except KeyboardInterrupt:
                print("\nStopping audio detection.")
                break
            
except Exception as e:
    print(f"Error: {e}")
    print("Check if your audio device is properly connected and configured")
