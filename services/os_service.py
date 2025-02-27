from os import environ, system as os_system
from platform import system
from PIL import ImageGrab
from utils.load_environ import load_environ


class OSService:

    def __init__(self):
        load_environ()

    def set_environ(self, key, value):
        environ[key] = value

    def get_environ(self, key):
        return environ.get(key)

    def get_screen_shot(self):
        screenshot = ImageGrab.grab()
        path = self.get_environ("photo_name")
        screenshot.save(path)
        return open(path, "rb")

    def lock_screen(self):
        if system() == "Windows":
            os_system("rundll32.exe user32.dll,LockWorkStation")
        elif system() == "Linux":
            os_system(
                "dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock")
        elif system() == "Darwin":
            os_system("pmset displaysleepnow")

    def turn_off(self):
        if system() == "Windows":
            os_system("shutdown /s /t 1")
        elif system() == "Linux":
            os_system("poweroff")
        elif system() == "Darwin":
            os_system("shutdown -h now")
