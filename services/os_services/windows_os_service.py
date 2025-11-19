from os import system as os_system
from PIL import ImageGrab


class WindowsOSService(BaseOSService):

    def get_screen_shot(self):
        path = "screenshot.png"
        ImageGrab.grab().save(path, "PNG")
        return open(path, "rb")

    def lock_screen(self):
        os_system("rundll32.exe user32.dll,LockWorkStation")

    def turn_off(self):
        os_system("shutdown /s /t 1")

    def mute_system(self):
        os_system("nircmd mutesysvolume 1")

    def unmute_system(self):
        os_system("nircmd mutesysvolume 0")
