from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.switch import Switch
from kivy.clock import Clock
import os

from selection_page import SelectionPage
from login_signup_page import LoginSignUpPage
from login_page import LoginPage
from signup_page import SignUpPage
from dashboard_page import DashboardPage
from document_reader_page import DocumentReaderPage
from object_recognition_page import ObjectRecognitionPage
from text_to_speech_page import TextRecognitionPage

class MyApp(App):
    def build(self):
        self.sm = ScreenManager(transition=SlideTransition())

        self.sm.add_widget(SelectionPage(name="selection_page"))
        self.sm.add_widget(LoginSignUpPage(name="login_signup_page"))
        self.sm.add_widget(LoginPage(name="login_page"))
        self.sm.add_widget(SignUpPage(name="signup_page"))
        self.sm.add_widget(DashboardPage(name="dashboard_page"))
        self.sm.add_widget(DocumentReaderPage(name="document_reader_page"))
        self.sm.add_widget(ObjectRecognitionPage(name="object_recognition_page"))
        self.sm.add_widget(TextRecognitionPage(name="text_to_speech_page"))

        # Ensure image files exist
        self.bg_white = "bgwhite.jpg"
        self.bg_black = "bgblack.jpg"
        if not os.path.exists(self.bg_white) or not os.path.exists(self.bg_black):
            print("Error: Background images not found!")

        self.background = Image(source=self.bg_white, allow_stretch=True, keep_ratio=False)
        
        # Floating layout to hold buttons
        float_layout = FloatLayout()

        # Back Button
        back_button = Button(
            background_normal="back.png",
            size_hint=(None, None),
            size=(60, 60),
            pos_hint={"x": 0.02, "top": 0.98}
        )
        back_button.bind(on_press=self.go_back)
        float_layout.add_widget(back_button)

        # Switch Background Toggle Button
        self.bg_switch = Switch(
            active=False,
            size_hint=(None, None),
            size=(50, 30),
            pos_hint={"right": 0.98, "top": 0.98}
        )
        self.bg_switch.bind(active=self.toggle_background)
        float_layout.add_widget(self.bg_switch)

        # Root layout
        root_layout = FloatLayout()
        root_layout.add_widget(self.background)
        root_layout.add_widget(self.sm)
        root_layout.add_widget(float_layout)

        return root_layout

    def go_back(self, instance):
        if self.sm.current == "selection_page":
            print("Already on the first screen!")
        else:
            self.sm.transition.direction = 'right'
            previous_screen = self.get_previous_screen()
            if previous_screen:
                self.sm.current = previous_screen
                print(f"Going back to: {previous_screen}")

    def get_previous_screen(self):
        screen_list = ["selection_page", "login_signup_page", "login_page", "signup_page",
                       "dashboard_page", "document_reader_page", "object_recognition_page", "text_to_speech_page"]
        current_index = screen_list.index(self.sm.current)
        if current_index > 0:
            return screen_list[current_index - 1]
        return None

    def toggle_background(self, instance, value):
        if value:
            self.background.source = self.bg_black
        else:
            self.background.source = self.bg_white
        
        Clock.schedule_once(lambda dt: self.background.reload(), 0.1)

if __name__ == "__main__":
    MyApp().run()
