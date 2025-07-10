# Object Detection with Bluetooth Audio Alerts

> A real-time object detection system on NVIDIA Jetson that sends **spoken alerts** to a connected **Bluetooth speaker** when specific objects (like humans, animals, or vehicles) are detected.

![Object Detection in Action](https://example.com/your-image-link.jpg)  
<!-- 🔄 Replace with your actual image or GIF link -->

---

## 🧠 The Algorithm

This project uses the `jetson.inference` library with the **SSD-Mobilenet-v2** model to detect objects from a live camera feed on a Jetson device.

When an object (e.g., a human, cat, dog, or vehicle) is detected with a confidence score above a threshold, the system announces it using `espeak` (text-to-speech) over a **Bluetooth audio device**.

### 💡 How It Works:
1. **Camera Input**  
   CSI or USB camera feeds are captured using `jetson.utils.videoSource`.

2. **Object Detection**  
   The `jetson.inference.detectNet` model processes each frame using SSD-Mobilenet-v2.

3. **Cooldown Mechanism**  
   Repeated detections are throttled with a cooldown timer to avoid audio spamming.

4. **Audio Alerts**  
   When an object passes the confidence threshold, a corresponding phrase is spoken via `espeak`.

5. **Bluetooth Audio**  
   Alerts are routed to a paired Bluetooth speaker or headset using `bluez` and `pulseaudio`.

---

## 🔧 Installation & Dependencies

### 🧱 System Dependencies
Install core libraries, Bluetooth tools, and audio support:

```bash
sudo apt update
sudo apt install -y \
  git build-essential cmake \
  bc bison flex \
  libssl-dev libncurses5-dev libelf-dev \
  linux-modules-extra-$(uname -r) \
  espeak \
  pavucontrol \
  bluetooth bluez blueman pulseaudio \
  pulseaudio-module-bluetooth
pip3 install --upgrade jetson-stats
pip3 install numpy torch torchvision torchaudio
pip install winrt-Windows.Devices.Bluetooth.Rfcomm
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
cmake ../
make -j$(nproc)
sudo make install
sudo ldconfig

### Run human_detect.py
python3 detect_human.py /dev/video0 webrtc://@:8554/output
