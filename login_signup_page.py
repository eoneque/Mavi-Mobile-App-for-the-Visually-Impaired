from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

class LoginSignUpPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Image(source='logs.png', size_hint=(1, 0.3)))

        btn_login = Button(text="Log In", size_hint=(1, 0.2))
        btn_login.bind(on_release=lambda x: setattr(self.manager, "current", "login_page"))  # ✅ Fix here

        btn_signup = Button(text="Sign Up", size_hint=(1, 0.2))
        btn_signup.bind(on_release=lambda x: setattr(self.manager, "current", "signup_page"))  # ✅ Fix here

        layout.add_widget(btn_login)
        layout.add_widget(btn_signup)
        self.add_widget(layout)
