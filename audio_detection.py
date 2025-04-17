# -*- coding: utf-8 -*-
import sounddevice as sd
import numpy as np

def list_input_devices():
    devices = sd.query_devices()
    input_devices = []

    print("Các thiết bị đầu vào khả dụng:\n")
    for idx, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            print(f"[{idx}] {dev['name']} | Kênh: {dev['max_input_channels']} | Sample rate mặc định: {int(dev['default_samplerate'])} Hz")
            input_devices.append((idx, dev))
    return input_devices

def main():
    # Liệt kê thiết bị và yêu cầu người dùng chọn
    input_devices = list_input_devices()
    if not input_devices:
        print("❌ Không tìm thấy thiết bị đầu vào nào.")
        return

    selected_id = int(input("\nNhập ID thiết bị bạn muốn sử dụng: "))
    
    try:
        selected_dev = sd.query_devices(selected_id)
        print(f"\n✅ Đang sử dụng thiết bị: {selected_dev['name']}")
    except Exception as e:
        print(f"Lỗi: {e}")
        return

    # Lấy thông tin cấu hình từ thiết bị
    channels = selected_dev['max_input_channels']
    samplerate = int(selected_dev['default_samplerate'])

    # Các tham số cấu hình
    CHUNK = 1024
    FORMAT = 'int16'  # tương thích tốt
    THRESHOLD = 75

    audio_detected = 0

    try:
        stream = sd.InputStream(
            device=selected_id,
            channels=channels,
            samplerate=samplerate,
            dtype=FORMAT
        )

        with stream:
            print(f"\n🎧 Đang lắng nghe âm thanh từ '{selected_dev['name']}'... Nhấn Ctrl+C để thoát.\n")
            while True:
                indata_raw, _ = stream.read(CHUNK)
                indata = np.abs(indata_raw).mean()

                if indata > THRESHOLD:
                    audio_detected = 1
                else:
                    audio_detected = 0

                print(f"Phát hiện âm thanh: {audio_detected} | Mức độ: {indata:.2f}")
    except KeyboardInterrupt:
        print("🛑 Dừng phát hiện âm thanh.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

if __name__ == '__main__':
    main()
