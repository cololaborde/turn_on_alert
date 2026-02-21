import shutil
from os import system as os_system, environ as os_environ
from PIL import ImageGrab
from services.os_services.base_os_service import BaseOSService
import subprocess

LOCKERS = {
    "hyprland": {
        "env": lambda: os_environ.get("HYPRLAND_INSTANCE_SIGNATURE"),
        "commands": [["hyprlock"]],
    },
    "sway": {
        "env": lambda: os_environ.get("XDG_CURRENT_DESKTOP", "").lower() == "sway",
        "commands": [["swaylock"]],
    },
    "wayland-generic": {
        "env": lambda: os_environ.get("XDG_SESSION_TYPE") == "wayland",
        "commands": [["swaylock"]],
    },
    "x11": {
        "env": lambda: os_environ.get("XDG_SESSION_TYPE") == "x11",
        "commands": [["i3lock"]],
    },
    "gnome": {
        "env": lambda: "gnome" in os_environ.get("XDG_CURRENT_DESKTOP", "").lower(),
        "commands": [["gnome-screensaver-command", "-l"]],
    },
    "xfce": {
        "env": lambda: "xfce" in os_environ.get("XDG_CURRENT_DESKTOP", "").lower(),
        "commands": [["xflock4"]],
    },
}



class LinuxOSService(BaseOSService):

    def command_exists(self, cmd):
        return shutil.which(cmd[0]) is not None

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
        for locker in LOCKERS.values():
            if locker["env"]():
                for cmd in locker["commands"]:
                    if self.command_exists(cmd):
                        subprocess.run(cmd)
                        return

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
