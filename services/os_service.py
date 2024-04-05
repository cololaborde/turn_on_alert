import os

from load_environ import load_environ

class OSService:

    def __init__(self):
        load_environ()
    
    def get_environ(self, key):
        return os.environ.get(key)

    def get_screen_shot(self):
        os.system("gnome-screenshot -f /home/colo/ptoa_rdk.png")
        # os.system("gnome-screenshot -f C:/Users/colo_/ptoa_rdk.png")
        return open("/home/colo/ptoa_rdk.png", "rb")
        # return "C:/Users/colo_/ptoa_rdk.png"
