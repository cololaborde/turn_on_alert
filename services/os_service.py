import os
import platform
from PIL import ImageGrab
from utils.load_environ import load_environ


class OSService:

    def __init__(self):
        load_environ()

    def get_environ(self, key):
        return os.environ.get(key)

    def get_screen_shot(self):
        screenshot = ImageGrab.grab()
        if platform.system() == "Windows":
            path = "C:/Users/colo/ptoa_rdk.png"
        elif platform.system() == "Linux":
            path = "/home/colo/ptoa_rdk.png"
        screenshot.save(path)
        return open(path, "rb")

    def lock_screen(self):
        if platform.system() == "Windows":
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif platform.system() == "Linux":
            os.system(
                "dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock")
        elif platform.system() == "Darwin":
            os.system("pmset displaysleepnow")

    def turn_off(self):
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        elif platform.system() == "Linux":
            os.system("poweroff")
        elif platform.system() == "Darwin":
            os.system("shutdown -h now")
