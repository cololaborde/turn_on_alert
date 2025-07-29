from os import environ, system as os_system
from platform import system
from PIL import ImageGrab
from utils.load_environ import load_environ


class OSService:

    def __init__(self):
        load_environ()
        self.system = system()

    def set_environ(self, key, value):
        environ[key] = value

    def get_environ(self, key):
        return environ.get(key)

    def get_screen_shot(self):
        path = self.get_environ("photo_name") or "screenshot.png"
        if self.system == "Windows":
            try:
                ImageGrab.grab().save(path, "PNG")
            except Exception as e:
                print(f"Error al tomar la captura de pantalla: {e}")
        elif self.system == "Linux":
            try:
                os_system(f"gnome-screenshot -f {path}")
            except Exception as e:
                print(f"Error al tomar la captura de pantalla: {e}")
        elif self.system == "Darwin":
            try:
                os_system(f"screencapture -x {path}")
            except Exception as e:
                print(f"Error al tomar la captura de pantalla: {e}")
        return open(path, "rb")

    def lock_screen(self):
        if self.system == "Windows":
            os_system("rundll32.exe user32.dll,LockWorkStation")
        elif self.system == "Linux":
            os_system(
                "dbus-send --type=method_call --dest=org.gnome.ScreenSaver /org/gnome/ScreenSaver org.gnome.ScreenSaver.Lock")
        elif self.system == "Darwin":
            os_system("pmset displaysleepnow")

    def turn_off(self):
        if self.system == "Windows":
            os_system("shutdown /s /t 1")
        elif self.system == "Linux":
            os_system("poweroff")
        elif self.system == "Darwin":
            os_system("shutdown -h now")

    def mute_system(self):
        if self.system == "Windows":
            os_system("nircmd mutesysvolume 1")
        elif self.system == "Linux":
            os_system("amixer set Master mute")
        elif self.system == "Darwin":
            os_system("osascript -e 'set volume output muted true'")

    def unmute_system(self):
        if self.system == "Windows":
            os_system("nircmd mutesysvolume 0")
        elif self.system == "Linux":
            os_system("amixer set Master unmute")
        elif self.system == "Darwin":
            os_system("osascript -e 'set volume output muted false'")
