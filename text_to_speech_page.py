import cv2
import easyocr
import numpy as np
import threading
import os
import random
import pygame
from gtts import gTTS
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from CameraManager import CameraManager  # Shared Camera Manager

# Initialize pygame mixer for playing audio
pygame.mixer.init()

def speak(text):
    """Use gTTS for speech and play it using pygame.mixer."""
    try:
        filename = f"temp_{random.randint(0, 99999)}.mp3"
        tts = gTTS(text=text, lang="tl")
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(filename)
    except Exception as e:
        print(f"⚠️ gTTS error: {e}")

class TextRecognitionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None
        self.is_scanning = True  # Auto-start scanning when page opens
        self.ocr_result = "Position object in front of the camera"
        self.reader = easyocr.Reader(['en'])
        self.scan_timer = 0  # Timer to track scanning duration

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.label = Label(text="Text Recognition", size_hint=(1, 0.1))
        layout.add_widget(self.label)

        self.image_widget = Image(size_hint=(1, 0.5))
        layout.add_widget(self.image_widget)

        scroll_view = ScrollView(size_hint=(1, 0.3))
        self.text_area = TextInput(
            text=self.ocr_result,
            readonly=True,
            size_hint_y=None,
            height=150,
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
        )
        scroll_view.add_widget(self.text_area)
        layout.add_widget(scroll_view)

        buttons_layout = BoxLayout(size_hint=(1, 0.2))
        self.capture_button = Button(text="Take Photo", size_hint=(0.5, 0.2))
        self.capture_button.bind(on_press=self.capture_photo)
        buttons_layout.add_widget(self.capture_button)
        
        self.read_aloud_button = Button(text="Read Aloud", size_hint=(0.5, 0.2))
        self.read_aloud_button.bind(on_press=self.read_aloud)
        buttons_layout.add_widget(self.read_aloud_button)
        
        layout.add_widget(buttons_layout)
        self.add_widget(layout)
        
        self.start_scan()
        Clock.schedule_interval(self.check_scan_timeout, 1)

    def start_scan(self):
        if not self.camera:
            self.camera = CameraManager()
        
        Clock.schedule_interval(self.update_camera_feed, 1.0 / 30.0)
        threading.Thread(target=self.scan_text, daemon=True).start()

    def scan_text(self):
        while self.is_scanning:
            if not self.camera:
                return

            ret, frame = self.camera.get_frame()
            if ret:
                self.scan_timer = 0  # Reset timer when text is being processed
                cropped_frame = self.extract_text_area(frame)
                preprocessed = self.preprocess_image(cropped_frame)
                results = self.reader.readtext(preprocessed)

                detected_text = " ".join([res[1] for res in results if res[2] >= 0.8])
                
                if detected_text:
                    self.is_scanning = False
                    Clock.schedule_once(lambda dt: self.display_text(detected_text))

    def check_scan_timeout(self, dt):
        """Check if scanning has exceeded 30 seconds without detection."""
        if self.is_scanning:
            self.scan_timer += 1
            if self.scan_timer >= 30:
                self.is_scanning = False
                message = "Cannot Scan Text Directly. Try Taking a Photo Instead."
                Clock.schedule_once(lambda dt: self.display_text(message))
                threading.Thread(target=speak, args=(message,), daemon=True).start()

    def capture_photo(self, instance):
        """Capture a photo and scan for text."""
        if self.camera:
            ret, frame = self.camera.get_frame()
            if ret:
                photo_path = "captured_photo.png"
                cv2.imwrite(photo_path, frame)
                self.label.text = f"Photo saved: {photo_path}"
                
                preprocessed = self.preprocess_image(frame)
                results = self.reader.readtext(preprocessed)
                detected_text = " ".join([res[1] for res in results if res[2] >= 0.8])
                Clock.schedule_once(lambda dt: self.display_text(detected_text))

    def read_aloud(self, instance):
        """Read aloud the detected text."""
        threading.Thread(target=speak, args=(self.ocr_result,), daemon=True).start()

    def extract_text_area(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_gray = np.array([0, 0, 180], dtype=np.uint8)
        upper_gray = np.array([180, 50, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_gray, upper_gray)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            return frame[y:y+h, x:x+w]
        return frame

    def preprocess_image(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(gray)

    def display_text(self, detected_text):
        self.ocr_result = f"Detected Text:\n{detected_text}" if detected_text else "No text detected"
        self.text_area.text = self.ocr_result

    def update_camera_feed(self, dt):
        if self.camera:
            ret, frame = self.camera.get_frame()
            if ret:
                buf = cv2.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image_widget.texture = texture

    def on_leave(self, *args):
        self.is_scanning = False
        Clock.unschedule(self.update_camera_feed)
        self.camera.release_camera()
