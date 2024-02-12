from .data import Data
import threading
import zmq
context = zmq.Context()

class ZmqData(Data):
    def __init__(self, room):
        super().__init__(room)
        self.latest = None
        self.stop = False
        self.socket = context.socket(zmq.SUB)
        self.socket.connect('tcp://localhost:5556')
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.room)
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def get_latest(self):
        return {
            'room': self.room,
            'text': self.latest if self.latest is not None else 'No Captions Available.'
        }
    
    def __del__(self):
        self.stop = True
        self.thread.join()
        self.socket.close()

    def run(self):
        while not self.stop:
            latest = self.socket.recv_string()
            _, text = latest.split(' ', 1)
            self.latest = text