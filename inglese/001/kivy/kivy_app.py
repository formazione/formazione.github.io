import os
import sys
from pathlib import Path
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ListProperty

# --- Existing core logic (adapted) ---
LOG_FILE = "exercise_log.txt"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller/Buildozer """
    # In Kivy/Buildozer, App.directory is often used for resources
    # For now, we'll keep the original logic, but this might need adjustment
    # when packaging with Buildozer.
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_exercises():
    """
    Returns a list of HTML files in the 'exercizes' directory.
    """
    exercizes_dir = resource_path("exercizes")
    if os.path.isdir(exercizes_dir):
        return [f for f in os.listdir(exercizes_dir) if f.endswith(".html")]
    return []

def update_log(exercise_name):
    """
    Updates the log file with the exercise open count and date.
    """
    log_data = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    name, count, date = parts
                    log_data[name] = {"count": int(count), "date": date}

    if exercise_name in log_data:
        log_data[exercise_name]["count"] += 1
        log_data[exercise_name]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        log_data[exercise_name] = {"count": 1, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    with open(LOG_FILE, "w") as f:
        for name, data in log_data.items():
            f.write(f"{name},{data['count']},{data['date']}\n")

# --- Kivy UI ---

from kivy.utils import platform
import webbrowser

# Conditional import for Android WebView
if platform == 'android':
    try:
        from jnius import autoclass
        from android.runnable import run_on_ui_thread

        # Autoclass the necessary Android classes
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        activity = autoclass('org.kivy.android.PythonActivity').mActivity

        class AndroidWebView(Widget):
            def __init__(self, url, **kwargs):
                super().__init__(**kwargs)
                self.url = url
                self.webview = None
                self.bind(pos=self._update_webview_layout, size=self._update_webview_layout)
                self.create_webview()

            @run_on_ui_thread
            def create_webview(self, *args):
                if self.webview is None:
                    self.webview = WebView(activity)
                    self.webview.getSettings().setJavaScriptEnabled(True)
                    self.webview.setWebViewClient(WebViewClient())
                    activity.addContentView(self.webview, autoclass('android.view.ViewGroup$LayoutParams')(-1, -1))
                    self.webview.loadUrl(self.url)
                    self._update_webview_layout()

            @run_on_ui_thread
            def _update_webview_layout(self, *args):
                if self.webview:
                    # Convert Kivy coordinates to Android coordinates
                    dp = self.dp
                    x, y = self.pos
                    width, height = self.size

                    # Kivy's y-coordinate is from bottom, Android's is from top
                    # Need to get the root window height to convert
                    from kivy.core.window import Window
                    android_height = Window.height

                    top = int(android_height - (y + height))
                    bottom = int(android_height - y)
                    left = int(x)
                    right = int(x + width)

                    self.webview.layout(left, top, right, bottom)

            def on_size(self, instance, value):
                self._update_webview_layout()

            def on_pos(self, instance, value):
                self._update_webview_layout()

            def on_parent(self, instance, value):
                if not value and self.webview:
                    # When the widget is removed from parent, remove the webview
                    self.webview.destroy()
                    self.webview = None

    except Exception as e:
        print(f"Error importing Android WebView components: {e}")
        AndroidWebView = None # Fallback if jnius fails
else:
    AndroidWebView = None # Not on Android


class ExerciseViewer(Popup):
    """
    A popup to display the exercise content.
    Uses AndroidWebView on Android, or opens in browser on desktop.
    """
    exercise_filepath = StringProperty("")

    def __init__(self, filepath, **kwargs):
        super().__init__(**kwargs)
        self.title = os.path.basename(filepath)
        self.exercise_filepath = filepath
        self.size_hint = (0.9, 0.9)
        self.content = BoxLayout(orientation='vertical')

        if platform == 'android' and AndroidWebView:
            # On Android, use the native WebView
            self.webview_widget = AndroidWebView(url=Path(filepath).as_uri())
            self.content.add_widget(self.webview_widget)
        else:
            # On desktop, open in default browser and show a message
            webbrowser.open(Path(filepath).as_uri())
            self.content.add_widget(Label(text=f"Opened {os.path.basename(filepath)} in your default browser.\n(HTML rendering not available in desktop Kivy)"))

        close_button = Button(text="Close", size_hint_y=None, height=40)
        close_button.bind(on_release=self.dismiss)
        self.content.add_widget(close_button)


class ExerciseListScreen(BoxLayout):
    exercises = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.add_widget(Label(text="English Exercises", size_hint_y=None, height=40))

        self.exercise_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.exercise_list_layout.bind(minimum_height=self.exercise_list_layout.setter('height'))

        self_scroll_view = ScrollView()
        self_scroll_view.add_widget(self.exercise_list_layout)
        self.add_widget(self_scroll_view)

        self.load_exercises()

    def load_exercises(self):
        self.exercises = get_exercises()
        if not self.exercises:
            self.exercise_list_layout.add_widget(Label(text="No exercises found in the 'exercizes' directory."))
        else:
            for exercise_name in self.exercises:
                btn = Button(text=exercise_name, size_hint_y=None, height=48)
                btn.bind(on_release=self.open_exercise)
                self.exercise_list_layout.add_widget(btn)

    def open_exercise(self, instance):
        exercise_name = instance.text
        exercizes_dir = resource_path("exercizes")
        filepath = os.path.join(exercizes_dir, exercise_name)

        update_log(exercise_name)

        # Placeholder for HTML display
        viewer = ExerciseViewer(filepath=filepath)
        viewer.open()


class EnglishExercisesApp(App):
    def build(self):
        self.title = "English Exercises"
        return ExerciseListScreen()

if __name__ == "__main__":
    EnglishExercisesApp().run()
