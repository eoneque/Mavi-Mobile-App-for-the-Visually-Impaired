from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle
import os

class LoginSignUpPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Get the correct path for the background image
        bg_path = os.path.abspath("bgwhite.jpg")  # Ensure the image is in your project folder

        # Create a RelativeLayout to allow background placement
        layout = RelativeLayout()

        # Background Image using Rectangle
        with layout.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # White fallback
            self.bg_rect = Rectangle(source=bg_path, pos=self.pos, size=self.size)

        # Bind the background to window size changes
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Box layout for UI components
        box = BoxLayout(orientation='vertical', spacing=20, padding=20)
        box.size_hint = (0.8, 0.8)
        box.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # Logo Image
        logo = Image(source='logs.png', size_hint=(1, 0.3))

        # Log In Button
        btn_login = Button(
            text="Log In",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_login.bind(on_release=lambda x: setattr(self.manager, "current", "login_page"))

        # Sign Up Button
        btn_signup = Button(
            text="Sign Up",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        btn_signup.bind(on_release=lambda x: setattr(self.manager, "current", "signup_page"))

        # Add widgets to BoxLayout
        box.add_widget(logo)
        box.add_widget(btn_login)
        box.add_widget(btn_signup)

        # Add BoxLayout to the main layout
        layout.add_widget(box)
        self.add_widget(layout)

    def update_bg(self, *args):
        """Update background image position and size when the window resizes."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
