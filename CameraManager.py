import cv2

class CameraManager:
    _instance = None  # Singleton instance

    def __new__(cls, video_source=0):
        if cls._instance is None:
            cls._instance = super(CameraManager, cls).__new__(cls)
            cls._instance.video_source = video_source
            cls._instance.capture = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)  # ✅ Use DirectShow for better Windows compatibility

            # ✅ Set High-Quality Resolution
            cls._instance.set_resolution(1280, 720)  # Change to (1920, 1080) if needed

            if not cls._instance.capture.isOpened():
                print("⚠️ Error: Could not access the camera.")
        
        return cls._instance

    def set_resolution(self, width, height):
        """✅ Set camera resolution to improve quality."""
        if self.capture and self.capture.isOpened():
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            print(f"📷 Camera resolution set to {width}x{height}")

    def get_frame(self):
        """Retrieve a frame from the camera with optimized settings."""
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()

            # ✅ Reduce frame size dynamically if lag is detected
            if ret:
                frame = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_AREA)  # Smooth downscaling
                return ret, frame
        return False, None

    def release_camera(self):
        """Release the camera."""
        if self.capture and self.capture.isOpened():
            self.capture.release()
            CameraManager._instance = None  # Reset singleton instance
