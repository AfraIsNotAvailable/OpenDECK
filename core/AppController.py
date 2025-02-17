"""AppController class for managing applications and sending key commands."""

import time
from ctypes import windll
import win32gui
from pywinauto import Application
from pywinauto.application import ProcessNotFoundError
from core.utils import load_app_shortcuts, wait_for_window

user32 = windll.user32
user32.SetProcessDPIAware()
full_screen_rect = (0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))


class AppController:
    """Class for managing applications and sending key commands."""

    def __init__(
        self,
        app_name: str,
        window_title_re: str = None,
        wait_time: float = 5.0,
        config_file: str = r"core\app_shortcuts.json",
        auto_connect: bool = True,
    ):
        self.app_name = app_name
        self.window_title_re = window_title_re
        self.wait_time = wait_time
        self.config_file = config_file

        # Load configuration and store shortcuts.
        config = load_app_shortcuts(config_file)
        self.app_config = config.get(app_name)
        if self.app_config is None:
            raise ValueError(f"No configuration found for app '{app_name}'")
        self.app_path = self.app_config.get("app_path")
        self.shortcuts = self.app_config.get("shortcuts", {})

        self.app = None
        self.window = None
        self.is_fullscreen = False
        if auto_connect:
            self.connect_app()

    def connect_app(self):
        """Connects to a running instance or starts a new one."""
        try:
            self.app = Application(backend="uia").connect(path=self.app_path)
        except ProcessNotFoundError:
            self.app = Application(backend="uia").start(self.app_path)
        self.refresh_window()

    def refresh_window(self):
        """Searches for and caches the window, restoring it if needed."""
        self.window = wait_for_window(
            self.app, wait_time=self.wait_time, title_re=self.window_title_re
        )
        if self.window.is_minimized():
            print("Window is minimized; restoring...")
            self.window.restore()
            time.sleep(1)
        if not self.window.is_visible():
            print("Window is hidden; attempting to restore...")
            self.window.restore()
            time.sleep(1)
        self.window.set_focus()

    def send_action(self, action: str):
        """Sends a key command corresponding to the given action."""
        # self.window.restore()
        self.window.set_focus()
        # self.window.click_input(coords=(10, 10))
        win32gui.SetForegroundWindow(self.window.handle)

        # For other actions, just send their key sequence without altering fullscreen state.
        key_seq = self.shortcuts.get(action)
        if not key_seq:
            print(f"No shortcut defined for action '{action}'")
            return
        try:
            self.window.type_keys(key_seq)
            # If the fullscreen action was sent, toggle the state
            if action == "fullscreen":
                self.is_fullscreen = not self.is_fullscreen

        except Exception as e:
            print(f"Error sending action '{action}': {e}. Refreshing window handle...")
            self.refresh_window()
            self.window.type_keys(key_seq)
            if action == "fullscreen":
                self.is_fullscreen = not self.is_fullscreen
