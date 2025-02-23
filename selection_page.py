from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

class SelectionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Image(source='logs.png', size_hint=(1, 1)))
        layout.add_widget(Label(text="WELCOME!", font_size=24))
        btn_student = Button(text="Get Started", size_hint=(1, 0.2))
        btn_student.bind(on_release=lambda x: setattr(self.manager, "current", "login_signup_page"))

       
        layout.add_widget(btn_student)
        self.add_widget(layout)
