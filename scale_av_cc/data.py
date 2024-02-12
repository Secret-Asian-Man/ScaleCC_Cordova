from abc import ABC, abstractmethod
from .textGenerator import build_entry

class Data(ABC):
    def __init__(self, room):
        self.room = room

    @abstractmethod
    def get_latest(self):
        pass

class RandomData(Data):
    def __init__(self, room):
        super().__init__(room)

    def get_latest(self):
        return {
            'room': self.room,
            'text': build_entry(),
        }
    
