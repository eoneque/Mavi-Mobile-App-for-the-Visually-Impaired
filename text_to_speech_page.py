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
        self.is_scanning = False  # Scanning starts only when page opens
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

        self.status_label = Label(text="", size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        buttons_layout = BoxLayout(size_hint=(1, 0.2))
        self.scan_button = Button(text="Start Scanning", size_hint=(0.33, 0.2))
        self.scan_button.bind(on_press=self.toggle_scan)
        buttons_layout.add_widget(self.scan_button)
        
        self.capture_button = Button(text="Take Photo", size_hint=(0.33, 0.2))
        self.capture_button.bind(on_press=self.capture_photo)
        buttons_layout.add_widget(self.capture_button)
        
        self.read_aloud_button = Button(text="Read Aloud", size_hint=(0.33, 0.2))
        self.read_aloud_button.bind(on_press=self.read_aloud)
        buttons_layout.add_widget(self.read_aloud_button)
        
        layout.add_widget(buttons_layout)
        self.add_widget(layout)

    def capture_photo(self, instance):
        """Capture an image from the camera and scan for text."""
        if self.camera:
            ret, frame = self.camera.get_frame()
            if ret:
                photo_path = "captured_photo.png"
                cv2.imwrite(photo_path, frame)
                self.label.text = f"Photo saved: {photo_path}"
                
                preprocessed = self.preprocess_image(frame)
                results = self.reader.readtext(preprocessed)
                detected_text = " ".join([res[1] for res in results if res[2] >= 0.8])
                
                if detected_text:
                    Clock.schedule_once(lambda dt: self.update_text_display(detected_text))
                else:
                    message = "No text detected. Try again."
                    Clock.schedule_once(lambda dt: self.update_text_display(message))
                    threading.Thread(target=speak, args=(message,), daemon=True).start()

    def on_enter(self):
        """Start scanning only when the page is opened."""
        self.start_scan()

    def toggle_scan(self, instance):
        if self.is_scanning:
            self.stop_scan()
        else:
            self.start_scan()

    def start_scan(self):
        if not self.camera:
            self.camera = CameraManager()
        self.is_scanning = True
        self.scan_button.text = "Stop Scanning"
        Clock.schedule_interval(self.update_camera_feed, 1.0 / 30.0)
        threading.Thread(target=self.scan_text, daemon=True).start()
        Clock.schedule_interval(self.check_scan_timeout, 1)

    def stop_scan(self):
        self.is_scanning = False
        self.scan_button.text = "Start Scanning"
        Clock.unschedule(self.update_camera_feed)

    def update_camera_feed(self, dt):
        """Update the camera feed display."""
        if self.camera:
            ret, frame = self.camera.get_frame()
            if ret:
                buf = cv2.flip(frame, 0).tobytes()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image_widget.texture = texture

    def read_aloud(self, instance):
        threading.Thread(target=speak, args=(self.ocr_result,), daemon=True).start()

    def on_leave(self, *args):
        self.is_scanning = False
        Clock.unschedule(self.update_camera_feed)
        if self.camera:
            self.camera.release_camera()
            self.camera = None
