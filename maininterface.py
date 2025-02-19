from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button


class Page1(Screen):
    pass


class Page2(Screen):
    pass


class Page3(Screen):
    pass


class Page4(Screen):
    pass


class MainApp(App):
    def build(self):
        # Screen manager handles sliding transitions
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(Page1(name="page1"))
        sm.add_widget(Page2(name="page2"))
        sm.add_widget(Page3(name="page3"))
        sm.add_widget(Page4(name="page4"))
        return sm

    def show_settings(self):
        # Create a popup for settings placeholder
        popup = Popup(
            title="Settings",
            content=Label(text="Settings Placeholder"),
            size_hint=(0.6, 0.4),
        )
        popup.open()


if __name__ == "_main_":
    MainApp().run()