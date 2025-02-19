from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle


class FontSizeSelectionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the white background for the screen
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=[20, 50, 20, 20], spacing=20)

        # FloatLayout for positioning the back button
        float_layout = FloatLayout(size_hint=(1, None), height=50)
        back_button = Button(
            text="<",
            size_hint=(0.1, 0.8),
            pos_hint={"x": 0, "y": 0.1},  # Position in the upper-left corner
            background_normal="",
            background_color=(0, 0, 0, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.on_back_button)
        float_layout.add_widget(back_button)

        # Add the FloatLayout (back button) to the main layout
        self.main_layout.add_widget(float_layout)

        # Center content
        self.center_layout = BoxLayout(orientation='vertical', spacing=10)

        # "Aa" Label
        self.aa_label = Label(
            text="Aa",
            font_size=50,  # Default font size
            color=(1, 0.8, 0, 1),  # Golden color
            size_hint_y=0.4
        )
        self.center_layout.add_widget(self.aa_label)

        # Font size question
        question_label = Label(
            text="What font size do you want?",
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint_y=0.2
        )
        self.center_layout.add_widget(question_label)
        self.main_layout.add_widget(self.center_layout)

        # Font size options
        options_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=0.4)

        small_button = Button(text="small", font_size=18, size_hint_y=0.2)
        small_button.bind(on_press=lambda instance: self.change_font_size(30))  # Small font size

        medium_button = Button(text="Medium", font_size=24, size_hint_y=0.2)
        medium_button.bind(on_press=lambda instance: self.change_font_size(50))  # Medium font size

        large_button = Button(text="Large", font_size=30, size_hint_y=0.2)
        large_button.bind(on_press=lambda instance: self.change_font_size(70))  # Large font size

        options_layout.add_widget(small_button)
        options_layout.add_widget(medium_button)
        options_layout.add_widget(large_button)

        # Add "Confirm" button
        confirm_button = Button(
            text="Confirm",
            font_size=20,
            size_hint_y=0.2,
            background_color=(0, 0.5, 0, 1),  # Green background
            color=(1, 1, 1, 1)  # White text
        )
        confirm_button.bind(on_press=self.on_confirm)

        options_layout.add_widget(confirm_button)

        self.main_layout.add_widget(options_layout)

        # Add main layout to the screen
        self.add_widget(self.main_layout)

        # To store the current font size
        self.selected_font_size = 50

    def _update_rect(self, *args):
        """Update the background rectangle when the window is resized or moved."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def change_font_size(self, size):
        """Change the font size of the Aa label."""
        self.selected_font_size = size
        self.aa_label.font_size = size

    def on_confirm(self, instance):
        """Handle the confirm button click."""
        print(f"Font size confirmed: {self.selected_font_size}")

    def on_back_button(self, instance):
        """Handle the back button (optional functionality)."""
        print("Back button pressed")  # Replace this with actual back navigation logic if needed


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FontSizeSelectionPage(name="font_size_selection"))
        return sm


if __name__ == "__main__":
    MyApp().run()
