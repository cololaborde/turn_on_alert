from abc import ABC, abstractmethod
from os import environ
from utils.load_environ import load_environ

class BaseOSService(ABC):

    def __init__(self):
        load_environ()

    @abstractmethod
    def get_screen_shot(self): ...

    @abstractmethod
    def lock_screen(self): ...

    @abstractmethod
    def turn_off(self): ...

    @abstractmethod
    def mute_system(self): ...

    @abstractmethod
    def unmute_system(self): ...

    def set_environ(self, key, value):
        environ[key] = value

    def get_environ(self, key):
        return environ.get(key)