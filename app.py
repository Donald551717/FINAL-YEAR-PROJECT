import streamlit as st
import os
import uuid
import tempfile
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import pyshark
import asyncio
import nest_asyncio
nest_asyncio.apply()


# Load model
model = load_model("malware_detection_cnn.h5")

# Prediction function
def predict_image(img_path):
    image = Image.open(img_path).convert("L")
    image = image.resize((64, 64))
    img_array = img_to_array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    confidence = float(np.max(prediction)) * 100
    class_index = int(np.argmax(prediction))
    return class_index, confidence

# Convert PCAP to images
def convert_pcap_to_images(pcap_file, output_dir):
    # ✅ Ensure a running event loop for pyshark
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    cap = pyshark.FileCapture(
        pcap_file,
        tshark_path='C:/Program Files/Wireshark/tshark.exe',
        use_json=True,
        include_raw=True
    )

    image_paths = []
    for i, pkt in enumerate(cap):
        try:
            raw_data = pkt.get_raw_packet()
            hex_data = raw_data.hex()
            byte_data = bytes.fromhex(hex_data)
            img_array = np.frombuffer(byte_data, dtype=np.uint8)

            # Pad and resize
            size = int(np.ceil(np.sqrt(len(img_array))))
            padded = np.zeros((size * size,), dtype=np.uint8)
            padded[:len(img_array)] = img_array
            img_matrix = padded.reshape((size, size))

            img = Image.fromarray(img_matrix)
            img = img.resize((64, 64)).convert("L")

            img_path = os.path.join(output_dir, f"pkt_{i}.png")
            img.save(img_path)
            image_paths.append(img_path)

        except Exception as e:
            print(f"[-] Skipped packet {i}: {e}")
            continue

    cap.close()
    return image_paths


# UI
st.title("🔍 AI Malware Detection (Encrypted Traffic)")
st.markdown("Upload either an **image or a `.pcap` file**. The system will detect if it's malware or benign.")

# --- Image Upload ---
st.header("📷 Upload an Image (.png)")
uploaded_image = st.file_uploader("Upload image", type=["png"], key="image")

if uploaded_image is not None:
    temp_img_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.png")
    with open(temp_img_path, "wb") as f:
        f.write(uploaded_image.read())

    st.image(temp_img_path, caption="🖼️ Uploaded Image", use_column_width=True)

    class_index, confidence = predict_image(temp_img_path)
    if class_index == 1:
        st.error(f"🚨 Detected: MALWARE ({confidence:.2f}% confidence)")
    else:
        st.success(f"✅ Detected: BENIGN ({confidence:.2f}% confidence)")

# --- PCAP Upload ---
st.header("🧪 Upload a PCAP File (.pcap)")
uploaded_pcap = st.file_uploader("Upload .pcap file", type=["pcap", "pcapng"], key="pcap")

if uploaded_pcap is not None:
    with st.spinner("⏳ Converting PCAP to images..."):
        temp_pcap_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.pcap")
        with open(temp_pcap_path, "wb") as f:
            f.write(uploaded_pcap.read())

        image_dir = os.path.join(tempfile.gettempdir(), f"pcap_images_{uuid.uuid4()}")
        os.makedirs(image_dir, exist_ok=True)
        images = convert_pcap_to_images(temp_pcap_path, image_dir)

    if images:
        st.success(f"✅ {len(images)} images created from PCAP.")
        results = {"Benign": 0, "Malware": 0}

        for img_path in images[:10]:  # scan only first 10 images for speed
            class_index, confidence = predict_image(img_path)
            label = "Malware" if class_index == 1 else "Benign"
            results[label] += 1

        st.write("🧾 **Prediction Summary (first 10 packets):**")
        st.write(f"🔹 Benign: {results['Benign']} / 10")
        st.write(f"🔸 Malware: {results['Malware']} / 10")

        if results["Malware"] > results["Benign"]:
            st.error("🚨 Suspicious traffic detected in this PCAP.")
        else:
            st.success("✅ PCAP looks mostly benign.")
    else:
        st.warning("⚠️ No valid packets found to analyze.")
