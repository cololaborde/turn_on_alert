import shutil
from os import system as os_system, environ as os_environ
from PIL import ImageGrab
from services.os_services.base_os_service import BaseOSService
import subprocess

LOCKERS = [
    ["loginctl", "lock-session"],
    ["hyprlock"],
    ["swaylock"],
    ["i3lock"],
    ["xflock4"],
]



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
        for cmd in LOCKERS:
            if shutil.which(cmd[0]):
                try:
                    subprocess.run(cmd, check=True)
                    return
                except Exception:
                    pass

        raise RuntimeError("No compatible lock screen found.")

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
