import time
from pywinauto import Application
from pywinauto.application import ProcessNotFoundError
from core.utils import load_app_shortcuts, wait_for_window  # Import from utils


def open_app_with_shortcuts(
    app_name: str,
    action_keys: list[str] = None,
    config_file: str = r"core\app_shortcuts.json",
    wait_time: float = 5.0,
    window_title_re: str = None,
) -> None:
    """
    Opens an application and sends a sequence of key commands.

    Parameters:
        app_name (str): The key for the application in the JSON config.
        action_keys (list[str], optional): List of action names to send.
        config_file (str): Path to the JSON configuration file.
        wait_time (float): Maximum wait time (in seconds) for the window.
        window_title_re (str, optional): Regex to match the window title.
    """
    config = load_app_shortcuts(config_file)
    app_config = config.get(app_name)
    if app_config is None:
        raise ValueError(f"No configuration found for app '{app_name}'")

    app_path = app_config.get("app_path")
    shortcuts = app_config.get("shortcuts", {})

    # Try connecting to a running instance first.
    try:
        if window_title_re:
            app = Application(backend="uia").connect(title_re=window_title_re)
        else:
            app = Application(backend="uia").connect(path=app_path)
    except ProcessNotFoundError:
        # If not running, start a new instance.
        app = Application(backend="uia").start(app_path)

    try:
        # Wait for a window (including hidden/tray ones) to become available.
        window = wait_for_window(app, wait_time=wait_time, title_re=window_title_re)
        # If the window is minimized, restore it.
        if window.is_minimized():
            print("Window is minimized; restoring...")
            window.restore()
            time.sleep(1)
        # If the window is hidden (e.g. in tray), try to restore it.
        if not window.is_visible():
            print("Window is hidden; attempting to restore...")
            window.restore()
            time.sleep(1)
        window.set_focus()
        if action_keys:
            for action in action_keys:
                key_seq = shortcuts.get(action)
                if key_seq:
                    window.type_keys(key_seq)
                    # time.sleep(0.5)  # Delay between commands
                else:
                    print(f"No shortcut defined for action '{action}'")
    except Exception as e:
        print(f"An error occurred while executing shortcuts: {e}")


def open_app(
    app_name: str,
    config_file: str = r"core\app_shortcuts.json",
    wait_time: float = 5.0,
    window_title_re: str = None,
) -> None:
    """
    Opens an application.

    Parameters:
        app_name (str): The key for the application in the JSON config.
        config_file (str): Path to the JSON configuration file.
        wait_time (float): Maximum wait time (in seconds) for the window.
        window_title_re (str, optional): Regex to match the window title.
    """
    config = load_app_shortcuts(config_file)
    app_config = config.get(app_name)
    if app_config is None:
        raise ValueError(f"No configuration found for app '{app_name}'")

    app_path = app_config.get("app_path")

    # Try connecting to a running instance first.
    try:
        if window_title_re:
            app = Application(backend="uia").connect(title_re=window_title_re)
        else:
            app = Application(backend="uia").connect(path=app_path)
    except ProcessNotFoundError:
        # If not running, start a new instance.
        app = Application(backend="uia").start(app_path)

    try:
        # Wait for a window (including hidden/tray ones) to become available.
        window = wait_for_window(app, wait_time=wait_time, title_re=window_title_re)
        # If the window is minimized, restore it.
        if window.is_minimized():
            print("Window is minimized; restoring...")
            window.restore()
            time.sleep(1)
        # If the window is hidden (e.g. in tray), try to restore it.
        if not window.is_visible():
            print("Window is hidden; attempting to restore...")
            window.restore()
            time.sleep(1)
        window.set_focus()
    except Exception as e:
        print(f"An error occurred while opening the application: {e}")
