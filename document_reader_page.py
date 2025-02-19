import cv2
import os
import numpy as np
import threading
import platform
import random
import pygame  # For playing audio without FFmpeg
from gtts import gTTS  # Google Text-to-Speech
import mediapipe as mp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from CameraManager import CameraManager  # Shared Camera Manager

# ✅ Initialize pygame mixer (for playing audio)
pygame.mixer.init()

# ✅ Detect OS
IS_ANDROID = "android" in platform.system().lower()

# ✅ Use plyer for Android, gTTS + pygame for Windows/macOS/Linux
if IS_ANDROID:
    from plyer import tts  # Android TTS
    def speak(text):
        """Speak using Android TTS (Tagalog)."""
        try:
            tts.speak(text)
        except Exception as e:
            print(f"⚠️ TTS error: {e}")
else:
    def speak(text):
        """Use gTTS for Tagalog speech and play it using pygame.mixer."""
        try:
            filename = f"temp_{random.randint(0, 99999)}.mp3"
            tts = gTTS(text=text, lang="tl")
            tts.save(filename)

            # Play the generated speech file
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            # Wait until playback is finished
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            # Delete the file after playback
            os.remove(filename)

        except Exception as e:
            print(f"⚠️ gTTS error: {e}")

# ✅ Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detector = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# ✅ Load Face Recognition Model (EigenFace or FisherFace)
try:
    recognizer = cv2.face.EigenFaceRecognizer_create()  # Preferred model
except AttributeError:
    print("⚠️ EigenFaceRecognizer not found! Falling back to FisherFaceRecognizer.")
    recognizer = cv2.face.FisherFaceRecognizer_create()  # Backup model

if os.path.exists("trained_faces.xml"):
    recognizer.read("trained_faces.xml")  # Load trained model

# ✅ Load known faces dictionary (to map labels to names)
def load_known_faces(folder_path):
    label_map = {}
    label_index = 0
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.jpg', '.jpeg', '.png')):
            name = os.path.splitext(file_name)[0]
            label_map[label_index] = name
            label_index += 1
    return label_map

known_faces = load_known_faces("images")  # Load face labels

class DocumentReaderPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None  # Camera will only be initialized when needed
        self.is_scanning = False  # Scanning starts when the button is pressed

        # ✅ Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Image(source='logs.png', size_hint=(1, 0.3)))

        self.label = Label(text="Face Recognition", size_hint=(1, 0.1))  # UI in English
        layout.add_widget(self.label)

        # ✅ Video feed
        self.image_widget = Image()
        layout.add_widget(self.image_widget)

        # ✅ Scan Faces button
        self.btn_scan = Button(text="Scan Faces", size_hint=(1, 0.2))  # UI in English
        self.btn_scan.bind(on_press=self.start_scan)
        layout.add_widget(self.btn_scan)

        self.add_widget(layout)

    def start_scan(self, instance):
        """Start face scanning when the button is pressed."""
        if not self.camera:
            self.camera = CameraManager()  # Initialize camera if not already open

        self.label.text = "Scanning for faces..."  # UI in English
        self.is_scanning = True

        Clock.schedule_interval(self.update_video_feed, 1.0 / 30.0)
        threading.Thread(target=self.scan_faces, daemon=True).start()  # Run face detection in background

    def scan_faces(self):
        """Detect faces in the video feed using MediaPipe."""
        while self.is_scanning:
            if not self.camera:
                return

            ret, frame = self.camera.get_frame()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detector.process(rgb_frame)

                if not results.detections:
                    print("🔍 No faces detected.")
                    continue  # Skip if no faces found

                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    frame_h, frame_w, _ = frame.shape

                    x = max(0, int(bboxC.xmin * frame_w))
                    y = max(0, int(bboxC.ymin * frame_h))
                    w = max(1, int(bboxC.width * frame_w))
                    h = max(1, int(bboxC.height * frame_h))

                    x = min(x, frame_w - 1)
                    y = min(y, frame_h - 1)
                    w = min(w, frame_w - x)
                    h = min(h, frame_h - y)

                    face = rgb_frame[y:y + h, x:x + w]

                    if face.shape[0] > 20 and face.shape[1] > 20:
                        face = self.preprocess_face(face)

                        # ✅ Recognize Face
                        if face is not None:
                            label, confidence = recognizer.predict(face)
                            if confidence < 5000:  # Confidence threshold
                                name = known_faces.get(label, "Unknown")
                                Clock.schedule_once(lambda dt: self.successful_scan(name))

    def preprocess_face(self, face):
        """Preprocess face images for recognition."""
        face = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)  
        face = cv2.resize(face, (200, 200))
        return face

    def successful_scan(self, name):
        """Handle successful face detection and announce the recognized name in Tagalog."""
        self.is_scanning = False
        self.label.text = f"Recognized: {name}"  # UI in English

        # ✅ Announce in Tagalog
        greeting = f"This is, {name}" if name != "Unknown" else "Not Recognized"
        threading.Thread(target=speak, args=(greeting,), daemon=True).start()

        Clock.unschedule(self.update_video_feed)
        self.release_camera()

    def update_video_feed(self, dt):
        """Continuously update the video feed while scanning."""
        if not self.is_scanning or not self.camera:
            return

        ret, frame = self.camera.get_frame()
        if ret:
            buffer = cv2.flip(frame, 0).tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
            self.image_widget.texture = texture

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
