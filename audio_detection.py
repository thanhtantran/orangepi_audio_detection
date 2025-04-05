import sounddevice as sd
import numpy as np
import argparse

def main():
    # Tạo parser để xử lý tham số dòng lệnh
    parser = argparse.ArgumentParser(description='Audio detection with multiple device options')
    parser.add_argument('--device', type=int, choices=[1, 2], default=2,
                        help='1: Mic built-in (hw:2,0), 2: USB Sound (hw:3,0)')
    args = parser.parse_args()
    
    # Cấu hình thiết bị dựa trên lựa chọn
    if args.device == 1:
        # Mic built-in
        input_device = 'hw:2,0'
        CHANNELS = 2
        RATE = 8000
        print("Sử dụng mic built-in (hw:2,0)")
    else:
        # USB Sound
        input_device = 'hw:3,0'
        CHANNELS = 1
        RATE = 44100
        print("Sử dụng USB sound (hw:3,0)")
    
    # Các tham số chung
    FORMAT = 'int16'
    CHUNK = 1024
    THRESHOLD = 75
    
    # Biến theo dõi việc phát hiện âm thanh
    audio_detected = 0
    
    try:
        # Cấu hình luồng âm thanh
        stream = sd.InputStream(
            device=input_device,
            channels=CHANNELS,
            samplerate=RATE,
            dtype=FORMAT
        )
        
        with stream:
            print(f"Đang lắng nghe âm thanh từ {input_device}... Nhấn Ctrl+C để thoát.")
            while True:
                # Đọc dữ liệu âm thanh
                indata_raw, overflowed = stream.read(CHUNK)
                
                # Xử lý dữ liệu (tính giá trị trung bình)
                indata = np.abs(indata_raw).mean()
                
                # Kiểm tra phát hiện âm thanh
                if indata > THRESHOLD:
                    audio_detected = 1
                else:
                    audio_detected = 0
                
                # Hiển thị trạng thái
                print(f"Âm thanh được phát hiện: {audio_detected}, Mức độ: {indata}")
    
    except KeyboardInterrupt:
        print("Dừng phát hiện âm thanh.")
    except Exception as e:
        print(f"Lỗi: {e}")
        print("Kiểm tra xem thiết bị âm thanh có được kết nối và cấu hình đúng không")

if __name__ == "__main__":
    main()
