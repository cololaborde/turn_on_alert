from os import environ, system as os_system
from platform import system
from PIL import ImageGrab
import shutil
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
            ImageGrab.grab().save(path, "PNG")

        elif self.system == "Linux":
            # 1. Wayland (grim)
            if shutil.which("grim"):
                os_system(f"grim {path}")
            # 2. GNOME X11
            elif shutil.which("gnome-screenshot"):
                os_system(f"gnome-screenshot -f {path}")
            # 3. scrot (X11)
            elif shutil.which("scrot"):
                os_system(f"scrot {path}")
            # 4. maim (X11)
            elif shutil.which("maim"):
                os_system(f"maim {path}")
            # 5. fallback imagegrab (X11 only)
            else:
                try:
                    ImageGrab.grab().save(path, "PNG")
                except:
                    raise Exception("No hay herramienta disponible para capturas en este sistema.")

        elif self.system == "Darwin":
            os_system(f"screencapture -x {path}")

        return open(path, "rb")

    def lock_screen(self):
        if self.system == "Windows":
            os_system("rundll32.exe user32.dll,LockWorkStation")

        elif self.system == "Darwin":
            os_system("pmset displaysleepnow")

        elif self.system == "Linux":
            # 1. i3lock
            if shutil.which("i3lock"):
                os_system("i3lock")
            # 2. swaylock (Wayland)
            elif shutil.which("swaylock"):
                os_system("swaylock")
            # 3. GNOME
            elif shutil.which("gnome-screensaver-command"):
                os_system("gnome-screensaver-command -l")
            # 4. Cinnamon
            elif shutil.which("cinnamon-screensaver-command"):
                os_system("cinnamon-screensaver-command -l")
            # 5. MATE
            elif shutil.which("mate-screensaver-command"):
                os_system("mate-screensaver-command -l")
            # 6. XFCE
            elif shutil.which("xflock4"):
                os_system("xflock4")
            # 7. KDE Plasma
            elif shutil.which("qdbus"):
                os_system("qdbus org.freedesktop.ScreenSaver /ScreenSaver Lock")
            # 8. Omarchy
            elif shutil.which("omarchy-lock-screen"):
                os_system("omarchy-lock-screen")
            else:
                raise Exception("No se encontró ningún mecanismo para bloquear la pantalla en este sistema.")

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
