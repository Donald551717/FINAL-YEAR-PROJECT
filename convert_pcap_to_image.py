import os
import numpy as np
from PIL import Image
import pyshark

def bytes_to_image(byte_data, size=(64, 64)):
    byte_array = np.frombuffer(byte_data, dtype=np.uint8)
    padded = np.pad(byte_array, (0, size[0]*size[1] - len(byte_array)), mode='constant')
    img = padded[:size[0]*size[1]].reshape(size)
    return Image.fromarray(img.astype(np.uint8), 'L')

def process_pcap_to_images(pcap_file, output_dir):
    print(f"📥 Reading PCAP file: {pcap_file}")
    cap = pyshark.FileCapture(
        pcap_file,
        tshark_path='C:/Program Files/Wireshark/tshark.exe',
        use_json=True,
        include_raw=True
    )

    os.makedirs(output_dir, exist_ok=True)
    count = 0

    for i, pkt in enumerate(cap):
        try:
            raw = pkt.get_raw_packet()
            img = bytes_to_image(raw)
            img.save(os.path.join(output_dir, f"pkt_{i}.png"))
            print(f"[+] Saved pkt_{i}.png")
            count += 1
        except Exception as e:
            print(f"[-] Skipped packet {i}: {e}")
            continue

    cap.close()
    print(f"✅ Done. Total images created: {count}")

# Make sure this filename matches your real .pcap
# 👇 Make sure this file actually exists in the "pcaps" folder
pcap_path = "pcaps/benign_traffic.pcap"
output_path = "dataset/benign"

process_pcap_to_images(pcap_path, output_path)