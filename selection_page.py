from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
import os

class SelectionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Get the correct path for the background image
        bg_path = os.path.abspath("bgwhite.jpg")  # Ensure this image is in your project directory

        # Create a relative layout to hold everything
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
        logo = Image(source='logs.png', size_hint=(1, 0.4))

        # Label
        welcome_label = Label(text="WELCOME!", font_size=30, bold=True)

        # Styled Rounded Button
        btn_student = Button(
            text="Get Started",
            size_hint=(1, 0.15),
            background_color=(0.2, 0.6, 1, 1),  # Blue color
            color=(1, 1, 1, 1),  # White text
        )
        btn_student.bind(on_release=lambda x: setattr(self.manager, "current", "login_signup_page"))

        # Rounded effect for the button
        with btn_student.canvas.before:
            Color(0.2, 0.6, 1, 1)
            self.rounded_rect = RoundedRectangle(pos=btn_student.pos, size=btn_student.size, radius=[25])

        btn_student.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)

        # Adding widgets to layout
        box.add_widget(logo)
        box.add_widget(welcome_label)
        box.add_widget(btn_student)

        layout.add_widget(box)
        self.add_widget(layout)

    def update_bg(self, *args):
        """Update background image position and size when the window resizes."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def update_rounded_rect(self, instance, value):
        """Update the rounded rectangle for the button."""
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size
