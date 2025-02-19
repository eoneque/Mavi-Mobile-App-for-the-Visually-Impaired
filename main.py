from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

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
        self.sm.add_widget(LoginPage(name="login_page"))  # ✅ This is the correct name
        self.sm.add_widget(SignUpPage(name="signup_page"))
        self.sm.add_widget(DashboardPage(name="dashboard_page"))
        self.sm.add_widget(DocumentReaderPage(name="document_reader_page"))
        self.sm.add_widget(ObjectRecognitionPage(name="object_recognition_page"))
        self.sm.add_widget(TextRecognitionPage(name="text_to_speech_page"))

        # Adding a FloatLayout to overlay the button on top
        float_layout = FloatLayout()

        # Back Button with Image
        back_button = Button(
            background_normal="back.png",  # Use the PNG as the button image
            size_hint=(None, None),
            size=(60, 60),  # Adjust size as needed
            pos_hint={"x": 0.02, "top": 0.98}  # Positioning in top-left corner
        )
        
        back_button.bind(on_press=self.go_back)  # Bind function to go back

        float_layout.add_widget(back_button)
        
        # Adding button layout on top of screen manager
        root_layout = FloatLayout()
        root_layout.add_widget(self.sm)
        root_layout.add_widget(float_layout)

        return root_layout

    def go_back(self, instance):
        """Goes back to the previous screen if possible."""
        if self.sm.current == "selection_page":
            print("Already on the first screen!")  # Prevents going back if at first screen
        else:
            self.sm.transition.direction = 'right'  # Smooth transition
            previous_screen = self.get_previous_screen()
            if previous_screen:
                self.sm.current = previous_screen
                print(f"Going back to: {previous_screen}")

    def get_previous_screen(self):
        """Returns the previous screen in the stack."""
        screen_list = ["selection_page", "login_signup_page", "login_page", "signup_page",
                       "dashboard_page", "document_reader_page", "object_recognition_page","text_recognition_page"]

        # Find current screen index and return the previous one
        current_index = screen_list.index(self.sm.current)
        if current_index > 0:
            return screen_list[current_index - 1]
        return None  # No previous screen

if __name__ == "__main__":
    MyApp().run()
