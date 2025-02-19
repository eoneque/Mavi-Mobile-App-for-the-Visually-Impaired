from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Line

class CircularButton(ButtonBehavior, Image):
    pass

class FacialRecognitionApp(App):
    def build(self):
        # Set window size and background color
        Window.size = (360, 640)
        Window.clearcolor = (0.13, 0.13, 0.13, 1)  # Dark gray background

        # Main layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)

        # Top bar layout
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.08))
        back_button = Button(text="<", size_hint=(0.1, 1), font_size=20)
        user_icon = Button(text="\U0001F464", size_hint=(0.1, 1), font_size=20)
        top_bar.add_widget(back_button)
        top_bar.add_widget(Widget())  # Spacer
        top_bar.add_widget(user_icon)
        layout.add_widget(top_bar)

        # Title
        title_label = Label(text="Facial Recognition", font_size=24, color=(1, 1, 1, 1), size_hint=(1, 0.08))
        layout.add_widget(title_label)

        # Image placeholder
        image = Image(source="arnel.png", size_hint=(1, 0.7), allow_stretch=True)
        layout.add_widget(image)

        # Capture button
        capture_layout = RelativeLayout(size_hint=(1, 0.2))
        with capture_layout.canvas:
            Color(1, 1, 1, 1)
            Line(circle=(180, 80, 40), width=2)
        capture_button = Button(size_hint=(None, None), size=(80, 80), background_color=(0, 0, 0, 0),
                                 background_normal="", pos_hint={'center_x': 0.5, 'center_y': 0.5})
        capture_layout.add_widget(capture_button)
        layout.add_widget(capture_layout)

        return layout

if __name__ == "__main__":
    FacialRecognitionApp().run()
