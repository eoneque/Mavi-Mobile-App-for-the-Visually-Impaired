from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

class BaseScreen(Screen):
    shared_dark_mode = False  # Shared across all screens
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Background
        self.bg_light = "bgwhite.jpg"  # Light mode image
        self.bg_dark = "bgblack.jpg"   # Dark mode image
        
        with self.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # Default white background
            self.bg_rect = Rectangle(source=self.bg_light, pos=self.pos, size=self.size)
        
        # Bind size updates
        self.bind(size=self.update_bg, pos=self.update_bg)
        
        # Apply correct mode when initialized
        self.apply_dark_mode()

    def update_bg(self, *args):
        """Update background image when window resizes."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def apply_dark_mode(self):
        """Apply dark mode settings to the background and text colors."""
        self.bg_rect.source = self.bg_dark if self.shared_dark_mode else self.bg_light
        self.bg_rect.reload()
        
        # Call this method in subclasses to update their UI components
        self.update_ui_colors()

    def update_ui_colors(self):
        """Update UI elements like labels, buttons, etc. Override in subclasses."""
        pass  # Implement this in specific screens