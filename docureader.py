from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior

# Custom Image Button
class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class DocumentReaderApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')
        
        # Header Label (Document Reader)
        header_label = Label(text="Document Reader", font_size=32, size_hint=(1, None), height=50)
        
        # Scrollable Content Area (White container)
        content_area = ScrollView(size_hint=(1, 1), height=500)
        white_container = BoxLayout(size_hint_y=None, height=800)
        white_container.add_widget(Label(text="Document Content Goes Here", size_hint_y=None, height=200))
        content_area.add_widget(white_container)

        # Image Button (Scan Icon)
        scan_button = ImageButton(source="scan_icon.png", size_hint=(None, None), size=(100, 100), pos_hint={"center_x": 0.5})
        
        # Organize Layout
        root.add_widget(header_label)
        root.add_widget(content_area)
        root.add_widget(scan_button)

        return root

if __name__ == '__main__':
    DocumentReaderApp().run()
