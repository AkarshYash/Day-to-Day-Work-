# ECO_SENTINEL_LITE.py - AI Forest Guardian (Deforestation & Fire Detector)
# Tech Used: Python, OpenCV, YOLOv8 (Ultralytics), Firebase (optional), Twilio SMS (optional)

import cv2
import numpy as np
from ultralytics import YOLO
import time
import requests  # For API alerts
from datetime import datetime

# ===== CONFIG =====
USE_CAMERA = True          # False for video file
SEND_ALERTS = False        # Enable Twilio/Firebase (set keys below)
MODEL_TYPE = "yolov8n.pt"  # Pre-trained model (replace with custom trained)
THRESHOLD = 0.7            # Confidence threshold
ALERT_COOLDOWN = 60        # Seconds between alerts

# API Keys (replace with yours)
FIREBASE_URL = "https://your-project.firebaseio.com/"
TWILIO_SID = "ACxxx"
TWILIO_TOKEN = "xxx"
TWILIO_PHONE = "+123456789"

# ===== INIT =====
model = YOLO(MODEL_TYPE)
last_alert_time = 0

# Labels to detect (YOLOv8 default classes - customize for chainsaws/etc)
DANGER_CLASSES = {
    0: "person",          # Potential loggers
    1: "bicycle",         # Logging transport
    3: "car",             # Logging vehicle
    8: "truck",          
    10: "fire hydrant",   # Proxy for fire
    11: "stop sign",      # Proxy for equipment
}

# ===== FUNCTIONS =====
def send_alert(event_type, frame):
    global last_alert_time
    if time.time() - last_alert_time < ALERT_COOLDOWN:
        return
    
    print(f"ALERT: {event_type} detected!")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    cv2.imwrite(f"alert_{timestamp}.jpg", frame)
    
    if SEND_ALERTS:
        # Send to Firebase
        requests.post(FIREBASE_URL + "alerts.json", json={
            "type": event_type,
            "time": timestamp,
            "image_url": f"alert_{timestamp}.jpg"
        })
        
        # SMS via Twilio (uncomment to enable)
        # client = Client(TWILIO_SID, TWILIO_TOKEN)
        # client.messages.create(
        #     body=f"ECO ALERT: {event_type} detected!",
        #     from_=TWILIO_PHONE,
        #     to="YOUR_PHONE"
        # )
    
    last_alert_time = time.time()

def process_frame(frame):
    results = model(frame)[0]
    danger_detected = False
    
    for box in results.boxes:
        class_id = int(box.cls)
        conf = float(box.conf)
        
        if class_id in DANGER_CLASSES and conf > THRESHOLD:
            label = DANGER_CLASSES[class_id]
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Draw bounding box
            color = (0, 0, 255) if "fire" in label.lower() else (0, 165, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            
            # Trigger alert
            if not danger_detected:
                send_alert(f"Forest threat: {label}", frame)
                danger_detected = True
    
    return frame

# ===== MAIN LOOP =====
if USE_CAMERA:
    cap = cv2.VideoCapture(0)  # Webcam
else:
    cap = cv2.VideoCapture("forest_demo.mp4")  # Sample video

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    processed_frame = process_frame(frame)
    cv2.imshow("EcoSentinel Lite", processed_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
