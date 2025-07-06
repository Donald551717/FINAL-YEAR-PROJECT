import os
import dpkt
import numpy as np
from PIL import Image

def convert_pcap_to_images(pcap_path, output_dir="packet_images", img_size=(64, 64)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(pcap_path, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        for i, (ts, buf) in enumerate(pcap):
            # Convert each packet into bytes
            packet_bytes = np.frombuffer(buf, dtype=np.uint8)

            # Trim or pad to fit the image size
            flat_size = img_size[0] * img_size[1]
            if len(packet_bytes) > flat_size:
                packet_bytes = packet_bytes[:flat_size]
            else:
                packet_bytes = np.pad(packet_bytes, (0, flat_size - len(packet_bytes)), 'constant')

            # Reshape into image
            img_array = packet_bytes.reshape(img_size)

            # Convert to RGB image
            img = Image.fromarray(img_array.astype(np.uint8), mode='L').convert("RGB")

            # Save image
            img.save(os.path.join(output_dir, f"packet_{i}.png"))

    print(f"✅ Done! Converted packets saved in '{output_dir}'")

# 🔽 Trigger the function
convert_pcap_to_images("2021-09-02-Hancitor-with-Cobalt-Strike.pcap")
