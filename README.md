# 🔐 AI-Based Image Recognition for Malware Detection in Encrypted Communication

This project uses **deep learning and image recognition** to detect malware hidden inside encrypted network traffic like TLS, HTTPS, or SSH. Instead of looking inside the traffic (which is encrypted), this project converts the network flows into **images** and uses a CNN (Convolutional Neural Network) to classify them as either **malicious** or **benign**.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [How It Works](#how-it-works)
- [Demo](#demo)
- [Requirements](#requirements)
- [Setup on Windows (Step-by-Step)](#setup-on-windows-step-by-step)
- [How to Use the App](#how-to-use-the-app)
- [Dataset Guide](#dataset-guide)
- [Model Architecture](#model-architecture)
- [Folder Structure](#folder-structure)
- [License](#license)
- [Author](#author)

---

## 📖 Project Overview

Encryption makes it hard for traditional antivirus or firewall systems to see what's happening inside network traffic. This project solves that by:
- Converting captured traffic (`.pcap` files) into structured flows,
- Turning the flows into colored images,
- Classifying those images using a trained deep learning model.

All this is wrapped in a simple **Streamlit web app** you can run locally.

---

## ⚙️ How It Works (Summary)

1. You collect a `.pcap` file (e.g., from Wireshark).
2. A Python script converts that `.pcap` into a 64x64 RGB image.
3. The image is passed into a trained CNN model (`model.h5`).
4. The model predicts if the traffic is **malicious** or **benign**.
5. You see the result in your browser using a Streamlit app.

---

## 🎥 Demo

📸 *Coming soon: Screenshots or video of the app in action*

---

## 🧰 Requirements

- Windows 10 or 11
- Python 3.8 or higher
- pip (comes with Python)
- Git (optional but helpful)

---

## 💻 Setup on Windows (Step-by-Step)

### ✅ 1. Install Python

Download and install Python from https://www.python.org/downloads/windows/.

> ⚠️ During installation, make sure to **check the box that says “Add Python to PATH.”**

---

### ✅ 2. Download the Project

Option A: **Using Git** (recommended):

```cmd
git clone https://github.com/your-username/ai-malware-detector.git
cd ai-malware-detector

````

Option B: **Download ZIP manually**

* Click the green `Code` button → `Download ZIP`
* Right-click the ZIP file and **Extract All**
* Open the extracted folder in **Command Prompt or PowerShell**

---

### ✅ 3. Create a Virtual Environment

In your project folder:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

Your prompt should now start with `(venv)` – that means you're inside the environment.

---

### ✅ 4. Install the Required Libraries

```cmd
pip install -r requirements.txt
```

> This installs everything the app needs: TensorFlow, Streamlit, NumPy, etc.

---

### ✅ 5. Run the App

```cmd
streamlit run app.py
```

> A browser tab will open automatically. If not, copy the link from the terminal and paste it into your browser.

---

## 🧪 How to Use the App

1. Open the app in your browser.
2. Click **“Browse Files”** to upload a `.pcap` file.
3. The app will:

   * Convert it into an image
   * Load the trained model
   * Predict if the traffic is **malicious** or **benign**
4. You’ll see the result instantly.

---

## 📁 Dataset Guide

To train your own model, structure your dataset like this:

```
dataset/
├── benign/
│   ├── img1.png
│   ├── img2.png
│   └── ...
└── malware/
    ├── img1.png
    ├── img2.png
    └── ...
```

You can create images by using:

```cmd
python pcap_to_image.py --input path\to\your.pcap --output image.png
```

---

## 🧠 Model Architecture

The CNN model we used has:

* 3 convolutional layers with ReLU + MaxPooling
* 1 fully connected layer
* 1 output layer with Sigmoid (for binary classification)

Compiled with:

```python
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
```

It was trained on 64x64 color images generated from `.pcap` network traffic.

---

## 📂 Folder Structure

```
ai-malware-detector/
├── app.py                ← Streamlit app
├── pcap_to_image.py      ← Converts .pcap to image
├── train.py              ← CNN training script
├── model.h5              ← Trained model file
├── requirements.txt      ← Python libraries list
├── dataset/              ← Your training images
└── README.md             ← This file
```

---

---

## 👨‍🎓 Author

**Donald Oke**
Final Year Project – Department of Cybersecurity

---

```

---

```
