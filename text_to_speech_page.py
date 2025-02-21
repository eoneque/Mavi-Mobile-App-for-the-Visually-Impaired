import cv2
import easyocr
import numpy as np
import threading
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

class TextRecognitionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None  # Camera will initialize only when needed
        self.is_scanning = False
        self.ocr_result = "Position text in front of the camera"
        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.label = Label(text="Text Recognition", size_hint=(1, 0.1))
        layout.add_widget(self.label)

        # Camera Feed
        self.image_widget = Image(size_hint=(1, 0.5))
        layout.add_widget(self.image_widget)

        # Scrollable Text Area
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

        self.confidence_label = Label(text="Confidence: N/A", size_hint=(1, 0.1))
        layout.add_widget(self.confidence_label)

        # Buttons Layout (Start Scanning & Take Photo)
        buttons_layout = BoxLayout(size_hint=(1, 0.2))
        self.scan_button = Button(text="Start Scanning", size_hint=(0.5, 0.2))
        self.scan_button.bind(on_press=self.toggle_scan)
        buttons_layout.add_widget(self.scan_button)
        
        self.capture_button = Button(text="Take Photo", size_hint=(0.5, 0.2))
        self.capture_button.bind(on_press=self.capture_photo)
        buttons_layout.add_widget(self.capture_button)
        
        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def toggle_scan(self, instance):
        if self.is_scanning:
            self.stop_scan()
        else:
            self.start_scan()

    def start_scan(self):
        if not self.camera:
            self.camera = CameraManager()

        self.label.text = "Scanning for text..."
        self.scan_button.text = "Stop Scanning"
        self.is_scanning = True
        threading.Thread(target=self.scan_text, daemon=True).start()
        Clock.schedule_interval(self.update_camera_feed, 1.0 / 30.0)  # Update camera feed 30 FPS

    def stop_scan(self):
        self.is_scanning = False
        self.label.text = "Text Recognition"
        self.scan_button.text = "Start Scanning"
        Clock.unschedule(self.update_camera_feed)

    def scan_text(self):
        while self.is_scanning:
            if not self.camera:
                return

            ret, frame = self.camera.get_frame()
            if ret:
                cropped_frame = self.extract_text_area(frame)
                preprocessed = self.preprocess_image(cropped_frame)
                results = self.reader.readtext(preprocessed)

                detected_text = " ".join([res[1] for res in results if res[2] >= 0.8])  # Confidence threshold 80%
                avg_confidence = (sum([res[2] for res in results]) / len(results)) * 100 if results else 0
                
                if avg_confidence >= 50:
                    self.is_scanning = False  # Stop scanning when confidence is 70% or higher
                Clock.schedule_once(lambda dt: self.display_text(detected_text, avg_confidence))

    def extract_text_area(self, frame):
        """Automatically detect and crop the text area."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_gray = np.array([0, 0, 180], dtype=np.uint8)
        upper_gray = np.array([180, 50, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_gray, upper_gray)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            return frame[y:y+h, x:x+w]
        return frame  # Fallback if no text box is found

    def preprocess_image(self, frame):
        """Apply advanced preprocessing techniques to improve OCR accuracy."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        return enhanced

    def display_text(self, detected_text, confidence):
        self.ocr_result = f"Detected Text:\n{detected_text}" if detected_text else "No text detected"
        self.text_area.text = self.ocr_result
        self.confidence_label.text = f"Confidence: {confidence:.2f}%"

    def update_camera_feed(self, dt):
        """Update the camera feed in the UI."""
        if self.camera:
            ret, frame = self.camera.get_frame()
            if ret:
                buf = cv2.flip(frame, 0).tostring()
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.image_widget.texture = texture

     
    def capture_photo(self, instance):
        """Capture a photo, save it, and scan for text."""
        if self.camera:
            ret, frame = self.camera.get_frame()
            if ret:
                photo_path = "captured_photo.png"
                cv2.imwrite(photo_path, frame)
                self.label.text = f"Photo saved: {photo_path}"
                
                # Process and scan the captured image
                preprocessed = self.preprocess_image(frame)
                results = self.reader.readtext(preprocessed)
                
                detected_text = " ".join([res[1] for res in results if res[2] >= 0.8])  # Confidence threshold 80%
                avg_confidence = (sum([res[2] for res in results]) / len(results)) * 100 if results else 0
                
                Clock.schedule_once(lambda dt: self.display_text(detected_text, avg_confidence))

    def release_camera(self):
        if self.camera:
            self.camera.release_camera()
            self.camera = None

    def on_leave(self, *args):
        self.stop_scan()
        self.release_camera()
