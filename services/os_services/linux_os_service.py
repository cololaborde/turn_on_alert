import shutil
from os import system as os_system
from PIL import ImageGrab
from services.os_services.base_os_service import BaseOSService


class LinuxOSService(BaseOSService):

    def get_screen_shot(self):
        path = "screenshot.png"

        if shutil.which("grim"):
            os_system(f"grim {path}")
        elif shutil.which("gnome-screenshot"):
            os_system(f"gnome-screenshot -f {path}")
        elif shutil.which("scrot"):
            os_system(f"scrot {path}")
        elif shutil.which("maim"):
            os_system(f"maim {path}")
        else:
            ImageGrab.grab().save(path, "PNG")

        return open(path, "rb")

    def lock_screen(self):
        if shutil.which("i3lock"):
            os_system("i3lock")
        elif shutil.which("swaylock"):
            os_system("swaylock")
        elif shutil.which("gnome-screensaver-command"):
            os_system("gnome-screensaver-command -l")
        elif shutil.which("cinnamon-screensaver-command"):
            os_system("cinnamon-screensaver-command -l")
        elif shutil.which("mate-screensaver-command"):
            os_system("mate-screensaver-command -l")
        elif shutil.which("xflock4"):
            os_system("xflock4")
        elif shutil.which("qdbus"):
            os_system("qdbus org.freedesktop.ScreenSaver /ScreenSaver Lock")
        elif shutil.which("omarchy-lock-screen"):
            os_system("omarchy-lock-screen")
        else:
            raise Exception("No lock screen available.")

    def turn_off(self):
        os_system("poweroff")

    def mute_system(self):
        if shutil.which("pactl"):
            os_system("pactl set-sink-mute @DEFAULT_SINK@ 1")
        elif shutil.which("amixer"):
            os_system("amixer set Master mute")
        else:
            raise Exception("Cannot mute on this Linux.")

    def unmute_system(self):
        if shutil.which("pactl"):
            os_system("pactl set-sink-mute @DEFAULT_SINK@ 0")
        elif shutil.which("amixer"):
            os_system("amixer set Master unmute")
        else:
            raise Exception("Cannot unmute on this Linux.")
