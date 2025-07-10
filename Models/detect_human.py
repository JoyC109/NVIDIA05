#!/usr/bin/python3
import jetson.inference
import jetson.utils
import subprocess
import os
import time
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="camera input (e.g. /dev/video0 or csi://0)")
parser.add_argument("output", type=str, help="output stream/display (e.g. webrtc://@:8554/output or display://0)")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="detection model to use")
parser.add_argument("--threshold", type=float, default=0.6, help="minimum detection confidence")
opt = parser.parse_args()

# Load detection network
net = jetson.inference.detectNet(opt.network, threshold=opt.threshold)

# Set up video sources
camera = jetson.utils.videoSource(opt.input)
output = jetson.utils.videoOutput(opt.output)

# Cooldowns in seconds
notify_interval = 3       # human, cat, dog
danger_interval = 0.3     # vehicles, etc.

# Last spoken time per class
last_notify_times = {}

# Map ClassID to labels
labels = {
    1: "Human",
    2: "Bicycle",
    3: "Car",
    4: "Motorcycle",
    6: "Bus",
    7: "Train",
    8: "Truck",
    16: "Dog",
    17: "Cat"
}

try:
    while True:
        img = camera.Capture()
        detections = net.Detect(img)
        now = time.time()

        # Step 1: Check which objects are eligible to trigger speech (cooldown passed)
        new_trigger_ids = []
        for detect in detections:
            class_id = detect.ClassID
            confidence = detect.Confidence

            if class_id not in labels or confidence < opt.threshold:
                continue

            last_time = last_notify_times.get(class_id, 0)
            cooldown = notify_interval if class_id in [1, 16, 17] else danger_interval

            if (now - last_time) > cooldown:
                new_trigger_ids.append(class_id)

        # Step 2: If any object’s cooldown passed, speak about ALL visible objects
        if new_trigger_ids:
            # Update notify time for all triggered classes
            for class_id in new_trigger_ids:
                last_notify_times[class_id] = now

            # Get ALL object labels in this frame
            visible_labels = sorted(set(
                labels[d.ClassID] for d in detections
                if d.ClassID in labels and d.Confidence >= opt.threshold
            ))

            # Construct phrase
            if len(visible_labels) == 1:
                phrase = f"Warning. {visible_labels[0]} ahead"
            else:
                phrase = f"Warning. {' and '.join(visible_labels)} ahead"

            print(f"🔊 {phrase}")
            subprocess.Popen(['espeak', phrase])

        # Render camera stream
        output.Render(img)
        output.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

        if not camera.IsStreaming() or not output.IsStreaming():
            break

except KeyboardInterrupt:
    print("\n🛑 Detection stopped by user.")
