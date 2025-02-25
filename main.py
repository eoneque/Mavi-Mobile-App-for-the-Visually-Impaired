from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.switch import Switch
from kivy.properties import StringProperty
import json
import os
from dashboard_page import DashboardPage
from selection_page import SelectionPage
from login_signup_page import LoginSignUpPage
from login_page import LoginPage
from signup_page import SignUpPage
from document_reader_page import DocumentReaderPage
from object_recognition_page import ObjectRecognitionPage
from text_to_speech_page import TextRecognitionPage

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    return {"background": "bgblack.jpg"}  # Default to bgblack.jpg

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

class MyApp(App):
    settings = load_settings()
    background = StringProperty(settings["background"])  # Load saved background setting

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

        # Root layout to hold the background image and main UI
        self.root_layout = FloatLayout()

        # Background image
        self.bg_image = Image(source=self.background, allow_stretch=True, keep_ratio=False)
        self.root_layout.add_widget(self.bg_image)
        self.root_layout.add_widget(self.sm)

        # Overlay Layout for buttons
        self.float_layout = FloatLayout()

        # Only add the back button if it's not the dashboard or main screen
        def update_back_button(*args):
            # Remove previous back button if any
            for widget in self.float_layout.children[:]:
                if isinstance(widget, Button) and widget.background_normal == "back.png":
                    self.float_layout.remove_widget(widget)

            if self.sm.current not in ["dashboard_page", "main"]:
                back_button = Button(
                    background_normal="back.png",  # Use the PNG as the button image
                    size_hint=(None, None),
                    size=(60, 60),  # Adjust size as needed
                    pos_hint={"x": 0.02, "top": 0.98}  # Positioning in top-left corner
                )
                back_button.bind(on_press=self.go_back)
                self.float_layout.add_widget(back_button)

        self.sm.bind(current=update_back_button)

        # Switch Button (Always Visible)
        self.switch_button = Switch(size_hint=(None, None), size=(60, 30), pos_hint={"right": 0.98, "top": 0.98})
        self.switch_button.bind(active=self.toggle_background)
        self.float_layout.add_widget(self.switch_button)

        # Ensure background is applied correctly when loading
        self.switch_button.active = self.background == "bgblack.jpg"
        self.apply_background()

        self.root_layout.add_widget(self.float_layout)
        return self.root_layout

    def toggle_background(self, instance, value):
        """Toggles the background between bgblack.jpg and bgwhite.jpg permanently."""
        self.background = "bgblack.jpg" if value else "bgwhite.jpg"
        save_settings({"background": self.background})  # Save setting permanently
        self.apply_background()

    def apply_background(self):
        """Applies the background image based on the stored setting."""
        self.bg_image.source = self.background

    def go_back(self, instance):
        """Goes back to the previous screen if possible."""
        if self.sm.current == "selection_page":
            print("Already on the first screen!")
        else:
            self.sm.transition.direction = 'right'
            previous_screen = self.get_previous_screen()
            if previous_screen:
                self.sm.current = previous_screen
                print(f"Going back to: {previous_screen}")

    def get_previous_screen(self):
        """Returns the previous screen in the stack."""
        screen_list = ["selection_page", "login_signup_page", "login_page", "signup_page",
                       "dashboard_page", "document_reader_page", "object_recognition_page", "text_to_speech_page"]
        current_index = screen_list.index(self.sm.current)
        return screen_list[current_index - 1] if current_index > 0 else None

if __name__ == "__main__":
    MyApp().run()
