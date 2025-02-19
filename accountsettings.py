from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class AccessibilitySettingsPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create a main layout (vertical box)
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 50, 20, 20])
        
        # Top gray bar with back arrow and user icon
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10, padding=[10, 10])
        back_button = Button(
            text="<",
            size_hint=(0.2, 1),  # Increase size of the back button
            background_normal="",
            background_color=(0, 0, 0, 1),  # Black background
        )
        
        top_bar.add_widget(back_button)
        top_bar.add_widget(Label())  # Filler to center items
        
        # Add top bar to main layout
        main_layout.add_widget(top_bar)
        
        # Create grid layout for the buttons
        grid_layout = GridLayout(cols=2, spacing=20, size_hint=(1, 0.8))
        
        # Create buttons with icons and labels below them
        buttons_data = [
            ("Announcement", "announcement.jpg"),
            ("Adjust Speech Speed", "audio.jpg"),
            ("Adjust Font Size", "fonteditor.jpg"),
            ("Logout", "logout.jpg"),
        ]
        
        for text, icon_path in buttons_data:
            button_layout = BoxLayout(orientation='vertical', spacing=10)

            # Create a button with an image as its background
            icon_button = Button(
                background_normal=icon_path, 
                size_hint_y=0.7, 
                background_color=(1, 1, 1, 1)  # Set white background
            )
            icon_button.bind(on_press=self.on_icon_click)  # Bind the click event
            
            label = Label(text=text, size_hint_y=0.3, font_size=14)
            button_layout.add_widget(icon_button)
            button_layout.add_widget(label)
            grid_layout.add_widget(button_layout)
        
        # Add grid layout to main layout
        main_layout.add_widget(grid_layout)
        
        # Add main layout to the screen
        self.add_widget(main_layout)

    def on_icon_click(self, instance):
        print(f"Clicked on: {instance.background_normal}")  # Handle the click event

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(AccessibilitySettingsPage(name="accessibility_settings"))
        return sm

if __name__ == "__main__":
    MyApp().run()
