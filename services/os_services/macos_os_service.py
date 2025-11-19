from os import system as os_system
from PIL import ImageGrab


class MacOSService(BaseOSService):

    def get_screen_shot(self):
        path = "screenshot.png"
        os_system(f"screencapture -x {path}")
        return open(path, "rb")

    def lock_screen(self):
        # /System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend -> lock real
        os_system("pmset displaysleepnow") # apaga display

    def turn_off(self):
        os_system("shutdown -h now")

    def mute_system(self):
        os_system("osascript -e 'set volume output muted true'")

    def unmute_system(self):
        os_system("osascript -e 'set volume output muted false'")
