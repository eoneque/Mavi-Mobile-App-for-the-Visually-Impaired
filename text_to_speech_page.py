import cv2
import pytesseract
import numpy as np
import threading
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput  # ✅ For displaying OCR result as text
from kivy.uix.label import Label
from kivy.clock import Clock
from CameraManager import CameraManager  # Shared Camera Manager

# ✅ Set path to Tesseract (Windows only)
# Modify this if you have Tesseract installed in a different location
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class TextRecognitionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = None  # Camera will initialize only when needed
        self.is_scanning = False  # Start scanning only when button is pressed
        self.ocr_result = "Position object in front of the camera"

        # ✅ Layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.label = Label(text="Text Recognition", size_hint=(1, 0.1))
        layout.add_widget(self.label)

        # ✅ Text Area for OCR Results
        self.text_area = TextInput(
            text=self.ocr_result,
            size_hint=(1, 0.6),
            readonly=True,  # ✅ Prevent user from editing detected text
            background_color=(0.9, 0.9, 0.9, 1),  # Light background
            foreground_color=(0, 0, 0, 1),  # Black text
        )
        layout.add_widget(self.text_area)

        # ✅ Button to Start/Stop Scanning
        self.scan_button = Button(text="Start Scanning", size_hint=(1, 0.2))
        self.scan_button.bind(on_press=self.toggle_scan)
        layout.add_widget(self.scan_button)

        self.add_widget(layout)

    def toggle_scan(self, instance):
        """Toggle scanning state when button is pressed."""
        if self.is_scanning:
            self.stop_scan()
        else:
            self.start_scan()

    def start_scan(self):
        """Start text recognition when the button is pressed."""
        if not self.camera:
            self.camera = CameraManager()  # Initialize camera if not already open

        self.label.text = "Scanning for text..."
        self.scan_button.text = "Stop Scanning"  # ✅ Change button text
        self.is_scanning = True

        threading.Thread(target=self.scan_text, daemon=True).start()  # Run OCR in background

    def stop_scan(self):
        """Stop scanning and keep last detected text."""
        self.is_scanning = False
        self.label.text = "Text Recognition"
        self.scan_button.text = "Start Scanning"  # ✅ Change button text

    def scan_text(self):
        """Detect text in the video feed."""
        while self.is_scanning:
            if not self.camera:
                return

            ret, frame = self.camera.get_frame()
            if ret:
                # ✅ Preprocess image for better OCR results
                preprocessed = self.preprocess_image(frame)

                # ✅ Use Tesseract OCR with optimized settings
                detected_text = pytesseract.image_to_string(
                    preprocessed,
                    lang="eng",  # Change this if your text is not in English
                    config="--oem 3 --psm 6"  # Best OCR engine mode & PSM mode for block text
                ).strip()

                # ✅ Update detected text
                Clock.schedule_once(lambda dt: self.display_text(detected_text))

    def preprocess_image(self, frame):
        """Apply advanced preprocessing techniques to improve OCR accuracy."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # ✅ Step 1: Remove Noise using GaussianBlur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # ✅ Step 2: Apply Adaptive Thresholding (Binarization)
        processed = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )

        # ✅ Step 3: Morphological Operations (Dilate to Join Letters)
        kernel = np.ones((3, 3), np.uint8)
        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)

        return processed

    def display_text(self, detected_text):
        """Display detected text in the text area."""
        if detected_text:
            self.ocr_result = f"Detected Text:\n{detected_text}"
        else:
            self.ocr_result = "No text detected"

        self.text_area.text = self.ocr_result  # ✅ Update text area with OCR result

    def release_camera(self):
        """Ensure the camera is released properly."""
        if self.camera:
            self.camera.release_camera()
            self.camera = None

    def on_leave(self, *args):
        """Ensure the camera is released when leaving the page."""
        self.stop_scan()
        self.release_camera()
