
import zmq 
context = zmq.Context()

from .constants import PUBLISH_ADDRESS

if __name__ == '__main__':
    socket = context.socket(zmq.PUB)
    publish = PUBLISH_ADDRESS.replace("0.0.0.0", "127.0.0.1")
    print(f"[INFO] Connecting to: {publish}")
    socket.connect(publish)
    while True:
        room = input('Room: ')
        text = input('Text: ')
        print(f'{room} {text}')
        socket.send_string(f'{room} {text}')
