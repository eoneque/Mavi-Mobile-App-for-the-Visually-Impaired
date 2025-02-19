from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

class RoleSelectionApp(App):
    def build(self):
        # Root layout
        root = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title and description
        title_label = Label(
            text="Welcome User",
            font_size='24sp',
            bold=True,
            halign='center',
            valign='middle',
            size_hint=(1, 0.2)
        )
        title_label.bind(size=title_label.setter('text_size'))

        description_label = Label(
            text="Please select the role to proceed",
            font_size='16sp',
            halign='center',
            valign='middle',
            size_hint=(1, 0.1)
        )
        description_label.bind(size=description_label.setter('text_size'))

        root.add_widget(title_label)
        root.add_widget(description_label)

        # Middle layout for icons and buttons
        middle_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.7))

        # Student Button
        student_layout = BoxLayout(orientation='vertical', spacing=10)
        student_icon = Image(source='stud.png', size_hint=(1, 0.8))  # Replace with actual file
        student_button = Button(
            text="Student",
            size_hint=(1, 0.2),
            font_size='16sp',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            bold=True
        )
        student_layout.add_widget(student_icon)
        student_layout.add_widget(student_button)

        # Teacher Button
        teacher_layout = BoxLayout(orientation='vertical', spacing=10)
        teacher_icon = Image(source='teacher.png', size_hint=(1, 0.8))  # Replace with actual file
        teacher_button = Button(
            text="Teacher",
            size_hint=(1, 0.2),
            font_size='16sp',
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
            bold=True
        )
        teacher_layout.add_widget(teacher_icon)
        teacher_layout.add_widget(teacher_button)

        middle_layout.add_widget(student_layout)
        middle_layout.add_widget(teacher_layout)

        root.add_widget(middle_layout)

        return root


if __name__ == '__main__':
    RoleSelectionApp().run()
