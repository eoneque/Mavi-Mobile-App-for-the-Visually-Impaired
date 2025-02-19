import cv2
import numpy as np
import threading
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from ultralytics import YOLO
from CameraManager import CameraManager  # Import CameraManager

# ✅ Load YOLOv8 Model (Trained on COCO Dataset or Custom Dataset)
MODEL_PATH = "yolov8n.pt"  # Change this to your trained model if needed
model = YOLO(MODEL_PATH)  

class ObjectRecognitionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None  # Camera will be initialized when scanning starts
        self.is_scanning = False  # Flag to track scanning status

        # ✅ UI Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Image(source='logs.png', size_hint=(1, 0.3)))

        self.label = Label(text="Object Recognition")
        layout.add_widget(self.label)

        # ✅ Video feed widget
        self.image_widget = Image()
        layout.add_widget(self.image_widget)

        # ✅ Scan Objects Button
        self.btn_scan = Button(text="Scan Object", size_hint=(1, 0.2))
        self.btn_scan.bind(on_press=self.start_scan)
        layout.add_widget(self.btn_scan)

        self.add_widget(layout)

    def start_scan(self, instance):
        """Start object recognition using YOLOv8."""
        if not self.camera:
            self.camera = CameraManager()  # Initialize camera if not already open

        self.label.text = "Scanning for objects..."
        self.is_scanning = True

        Clock.schedule_interval(self.update_video_feed, 1.0 / 30.0)  # Update every frame
        threading.Thread(target=self.detect_objects, daemon=True).start()  # Run YOLOv8 in a separate thread

    def detect_objects(self):
        """Perform YOLOv8 object recognition in real-time."""
        while self.is_scanning:
            if not self.camera:
                return

            ret, frame = self.camera.get_frame()
            if ret:
                results = model(frame)  # Run YOLOv8 detection
                detections = results[0].boxes.data.cpu().numpy()  # Get detected objects

                # Draw bounding boxes on the frame
                for detection in detections:
                    x1, y1, x2, y2, conf, cls = map(int, detection[:6])  # Get box coords & class
                    label = f"{model.names[cls]}: {conf:.2f}"  # Get object name

                    # ✅ Draw Bounding Box
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # ✅ Update label with detected objects
                detected_objects = [model.names[int(d[5])] for d in detections]
                if detected_objects:
                    self.label.text = f"Detected: {', '.join(set(detected_objects))}"
                else:
                    self.label.text = "No objects detected"

    def update_video_feed(self, dt):
        """Continuously update the video feed while scanning."""
        if not self.is_scanning or not self.camera:
            return

        ret, frame = self.camera.get_frame()
        if ret:
            # Convert frame to texture for Kivy UI
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
            self.image_widget.texture = texture
        else:
            print("⚠️ Failed to read frame from camera. Restarting...")
            self.release_camera()
            self.camera = CameraManager()  # Reinitialize camera
            Clock.schedule_once(lambda dt: self.start_scan(None), 1)

    def release_camera(self):
        """Ensure the camera is released properly."""
        if self.camera:
            self.camera.release_camera()
            self.camera = None

    def on_leave(self, *args):
        """Ensure the camera is released when leaving the page."""
        self.is_scanning = False
        Clock.unschedule(self.update_video_feed)
        self.release_camera()
