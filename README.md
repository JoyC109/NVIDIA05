# Object Detection with Audio Alerts

> A real-time object detection system on NVIDIA Jetson that sends **spoken alerts** when specific objects (like humans, animals, or vehicles) are detected.

---

## 🧠 The Algorithm

This project uses the `jetson.inference` library with the **SSD-Mobilenet-v2** model to detect objects from a live camera feed on a Jetson device.

When an object (e.g., a human, cat, dog, or vehicle) is detected with a confidence score above a threshold, the system announces it using `espeak` (a text-to-speech engine).

### 💡 How It Works:
1. **Camera Input**  
   CSI or USB camera feeds are captured using `jetson.utils.videoSource`.

2. **Object Detection**  
   The `jetson.inference.detectNet` model processes each frame using SSD-Mobilenet-v2.

3. **Cooldown Mechanism**  
   Repeated detections are throttled with a cooldown timer to avoid audio spamming.

4. **Audio Alerts**  
   When an object passes the confidence threshold, a corresponding phrase is spoken using `espeak`.

---

## 🧠 AI Model: SSD-Mobilenet-v2

SSD-Mobilenet-v2 is a lightweight and fast object detection model designed to run efficiently on edge devices like NVIDIA Jetson.

- **SSD (Single Shot Multibox Detector)**  
  Divides the image into a grid and predicts bounding boxes + class labels for each cell, enabling fast real-time detection.

- **MobileNet (Backbone Network)**  
  Optimized for low-power and high-speed inference, making it ideal for embedded systems.

- **Dataset**: MSCOCO (Common Objects in Context)  
  - 330K+ labeled images  
  - 1.5M+ object instances  
  - 80 object classes, including:
    - ClassID 1: Human  
    - ClassID 2: Bicycle  
    - ClassID 3: Car  
    - ClassID 4: Motorcycle  
    - ...  
    - ClassID 80: Toaster

---

## 🔧 Installation, Setup, & Running the Detector

```bash
# Install system dependencies
sudo apt update
sudo apt install -y \
  git build-essential cmake \
  bc bison flex \
  libssl-dev libncurses5-dev libelf-dev \
  linux-modules-extra-$(uname -r) \
  espeak \
  pavucontrol

# Install Python packages
pip3 install --upgrade jetson-stats
pip3 install numpy torch torchvision torchaudio

# Clone and build jetson-inference
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig

# Run the object detection script
python3 detect_human.py /dev/video0 webrtc://@:8554/output
