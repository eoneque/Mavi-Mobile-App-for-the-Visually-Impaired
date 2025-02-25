import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Rectangle

class DashboardPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set the background image
        bg_path = os.path.abspath("bgwhite.jpg")  # Ensure the image exists in your project folder
        root_layout = RelativeLayout()
        with root_layout.canvas.before:
            self.bg_color = Color(1, 1, 1, 1)  # White fallback color
            self.bg_rect = Rectangle(source=bg_path, pos=self.pos, size=self.size)
        # Bind size and position updates
        self.bind(size=self.update_bg, pos=self.update_bg)
        
        # Main content layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Image(source='logs.png', size_hint=(1, 0.3)))
        
        carousel = Carousel(direction='right')
        
        btn_face_recognition = Button(
            background_normal='facerecogicon.png',
            size_hint=(1, 0.6)
        )
        btn_face_recognition.bind(on_release=lambda x: setattr(self.manager, "current", "document_reader_page"))
        
        btn_object_recognition = Button(
            background_normal='objectrecogicon.png',
            size_hint=(1, 0.6)
        )
        btn_object_recognition.bind(on_release=lambda x: setattr(self.manager, "current", "object_recognition_page"))
        
        btn_text_to_speech = Button(
            background_normal='ttsicon.png',
            size_hint=(1, 0.6)
        )
        btn_text_to_speech.bind(on_release=lambda x: setattr(self.manager, "current", "text_to_speech_page"))
        
        for btn in [btn_face_recognition, btn_object_recognition, btn_text_to_speech]:
            screen_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
            screen_layout.add_widget(btn)
            carousel.add_widget(screen_layout)
        
        layout.add_widget(carousel)
        root_layout.add_widget(layout)
        
        # User icon at the top left corner
        user_icon_layout = RelativeLayout(size_hint=(None, None), size=(80, 80), pos_hint={'x': 0.02, 'top': 0.98})
        user_icon_image = Image(source='usericon.png', size_hint=(1, 1))
        user_icon_button = Button(
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0)  # Transparent button overlay
        )
        user_icon_button.bind(on_release=lambda x: setattr(self.manager, "current", "accountsettings"))
        user_icon_layout.add_widget(user_icon_image)
        user_icon_layout.add_widget(user_icon_button)
        root_layout.add_widget(user_icon_layout)
        
        # Back button at the bottom left corner
        back_button = Button(
            background_normal='back.png',
            size_hint=(None, None),
            size=(70, 70),
            pos_hint={'x': 0.02, 'y': 0.02}
        )
        back_button.bind(on_release=lambda x: setattr(self.manager, "current", "selection_page"))
        root_layout.add_widget(back_button)
        
        self.add_widget(root_layout)
    
    def update_bg(self, *args):
        """Update background image position and size when the window changes."""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
