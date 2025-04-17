# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np
import re

THRESHOLD_DB = -35  # Ngưỡng phát hiện âm thanh (dBFS)

def list_input_devices():
    devices = sd.query_devices()
    input_devices = []
    print("\n🔊 Danh sách thiết bị âm thanh phần cứng (hw:x,x):\n")
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0 and 'hw:' in dev['name']:
            match = re.search(r'\(hw:\d+,\d+\)', dev['name'])
            if match:
                print(f"{len(input_devices)}: {dev['name']} (Channels: {dev['max_input_channels']}, Rate: {int(dev['default_samplerate'])} Hz)")
                input_devices.append({
                    'index': i,
                    'name': dev['name'],
                    'channels': dev['max_input_channels'],
                    'rate': int(dev['default_samplerate'])
                })
    return input_devices

def calculate_rms_db(indata):
    rms = np.sqrt(np.mean(np.square(indata)))
    db = 20 * np.log10(rms / 32767 + 1e-10)  # dBFS
    return db

def detect_audio(device_info):
    try:
        stream = sd.InputStream(
            device=device_info['index'],
            channels=device_info['channels'],
            samplerate=device_info['rate'],
            dtype='int16'
        )

        print(f"\n🎙️ Đang nghe từ thiết bị: {device_info['name']}")
        print("Nhấn 'q' rồi Enter để quay lại menu chọn thiết bị. Nhấn Ctrl+C để thoát.\n")
        print("Lưu ý: Mức tín hiệu được đo bằng dBFS (Decibel Full Scale, 0 là lớn nhất)\n")

        with stream:
            while True:
                user_input = input("Nhấn Enter để tiếp tục, hoặc gõ 'q' để quay lại: ")
                if user_input.strip().lower() == 'q':
                    break

                indata_raw, _ = stream.read(1024)
                indata = np.frombuffer(indata_raw, dtype=np.int16)
                rms_db = calculate_rms_db(indata)
                audio_detected = int(rms_db > THRESHOLD_DB)

                print(f"Âm thanh: {audio_detected} | Mức dB: {rms_db:.2f} dBFS")

    except Exception as e:
        print(f"Lỗi: {e}")

def main():
    while True:
        input_devices = list_input_devices()
        if not input_devices:
            print("⚠️ Không tìm thấy thiết bị đầu vào nào.")
            return

        try:
            choice = int(input("\nChọn thiết bị bằng số (hoặc nhấn Enter để thoát): ").strip())
            if 0 <= choice < len(input_devices):
                detect_audio(input_devices[choice])
            else:
                print("❌ Lựa chọn không hợp lệ.")
        except ValueError:
            print("👋 Thoát.")
            break

if __name__ == '__main__':
    main()
