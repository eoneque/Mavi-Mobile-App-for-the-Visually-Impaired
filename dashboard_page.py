from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel

class DashboardPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Image(source='logs.png', size_hint=(1, 0.3)))

        carousel = Carousel(direction='right')

        btn_face_recognition = Button(text="Face Recognition", size_hint=(1, 0.6))
        btn_face_recognition.bind(on_release=lambda x: setattr(self.manager, "current", "document_reader_page"))
        btn_object_recognition = Button(text="Object Recognition", size_hint=(1, 0.6))
        btn_object_recognition.bind(on_release=lambda x: setattr(self.manager, "current", "object_recognition_page"))
        btn_text_to_speech = Button(text="Text To Speech", size_hint=(1, 0.6))
        btn_text_to_speech.bind(on_release=lambda x: setattr(self.manager, "current", "text_to_speech_page"))
        for btn in [btn_face_recognition, btn_object_recognition, btn_text_to_speech]:
            screen_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
            screen_layout.add_widget(btn)
            carousel.add_widget(screen_layout)

        layout.add_widget(carousel)
        self.add_widget(layout)
