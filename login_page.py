import cv2
import os
import numpy as np
import threading
import requests
import mediapipe as mp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from CameraManager import CameraManager  # ✅ Camera Management Class

# ✅ Firebase Configuration
FIREBASE_DATABASE_URL = "https://project-mavii1-default-rtdb.firebaseio.com"

# ✅ Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
face_detector = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)

# ✅ EigenFace Recognizer (for Face Recognition)
recognizer = cv2.face.EigenFaceRecognizer_create()


class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.is_scanning = False
        self.recognizer_trained = False
        self.recognition_attempts = []
        self.max_attempts = 5
        self.confidence_threshold = 5000

        # ✅ UI Layout
        layout = BoxLayout(orientation='vertical', spacing=15, padding=40)

        # ✅ Login Fields (Smaller Text Fields)
        self.label = Label(text="Login", size_hint=(1, 0.05), font_size=24)
        layout.add_widget(self.label)

        self.full_name_input = TextInput(hint_text="Full Name", multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.full_name_input)

        self.password_input = TextInput(hint_text="Password", password=True, multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.password_input)

        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint=(1, 0.05))
        layout.add_widget(self.error_label)

        # ✅ Buttons for Manual Login & Face Login (Larger Buttons)
        button_layout = BoxLayout(orientation="vertical", spacing=10, size_hint=(1, 0.3))

        self.login_button = Button(text="Login", size_hint=(1, 0.3), font_size=18, bold=True)
        self.login_button.bind(on_press=self.login)
        button_layout.add_widget(self.login_button)

        self.face_login_button = Button(text="Use Face Recognition", size_hint=(1, 0.3), font_size=18, bold=True)
        self.face_login_button.bind(on_press=self.start_scan)
        button_layout.add_widget(self.face_login_button)

        layout.add_widget(button_layout)

        # ✅ Navigation Buttons (Larger Buttons)

        self.add_widget(layout)

        # ✅ Load & Train Faces on App Start
        self.known_faces, self.label_map = self.load_known_faces("images")

    def login(self, instance):
        """Manual Login using Firebase"""
        full_name = self.full_name_input.text.strip()
        password = self.password_input.text.strip()

        if not full_name or not password:
            self.error_label.text = "Enter Full Name and Password!"
            return

        db_url = f"{FIREBASE_DATABASE_URL}/users.json"
        response = requests.get(db_url)

        if response.status_code == 200 and response.json():
            users_data = response.json()
            for user_id, user_info in users_data.items():
                if user_info["full_name"] == full_name and user_info["password"] == password:
                    self.manager.current = "dashboard"
                    return

            self.error_label.text = "Invalid Full Name or Password!"
        else:
            self.error_label.text = "No users found!"

    def start_scan(self, instance):
        """Start face recognition login (No Camera Feed)."""
        if not self.recognizer_trained:
            self.error_label.text = "No trained faces found!"
            return

        self.is_scanning = True
        self.face_login_button.text = "Scanning..."

        if not self.camera:
            self.camera = CameraManager()

        threading.Thread(target=self.recognize_face, daemon=True).start()

    def recognize_face(self):
        """Recognize face and log in if matched (No Camera Feed)."""
        while self.is_scanning:
            if not self.camera:
                return

            ret, frame = self.camera.get_frame()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_detector.process(rgb_frame)

                if not results.detections:
                    continue

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

                        if self.recognizer_trained and face is not None:
                            label, confidence = recognizer.predict(face)

                            if confidence < self.confidence_threshold:
                                self.recognition_attempts.append(label)

                                if len(self.recognition_attempts) >= self.max_attempts:
                                    most_frequent = max(set(self.recognition_attempts),
                                                        key=self.recognition_attempts.count)
                                    user_name = self.label_map.get(most_frequent, "Unknown")

                                    Clock.schedule_once(lambda dt: self.successful_login(user_name))
                                    return
                            else:
                                self.recognition_attempts = [] 

    def preprocess_face(self, face):
        """Preprocess face for recognition."""
        face = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)  
        face = cv2.resize(face, (200, 200))
        return face

    def successful_login(self, name):
        """Stop scanning and switch to the dashboard once a face is recognized."""
        self.is_scanning = False
        self.label.text = f"Welcome, {name}!"
        self.face_login_button.text = "Use Face Recognition"
        self.manager.current = "dashboard_page"

    def load_known_faces(self, folder_path):
        """Load known faces for recognition."""
        known_faces, labels, label_map = [], [], {}

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        for idx, file_name in enumerate(os.listdir(folder_path)):
            if file_name.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(folder_path, file_name)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                image = cv2.resize(image, (200, 200))

                if image is not None:
                    known_faces.append(image)
                    labels.append(len(label_map))
                    label_map[len(label_map)] = os.path.splitext(file_name)[0]

        if known_faces:
            recognizer.train(known_faces, np.array(labels))
            recognizer.save("trained_faces.xml")
            self.recognizer_trained = True

        return known_faces, label_map
