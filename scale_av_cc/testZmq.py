import sys
import zmq 
context = zmq.Context()

from .constants import PUBLISH_ADDRESS

if __name__ == '__main__':
    socket = context.socket(zmq.PUB)
    publish = PUBLISH_ADDRESS.replace("0.0.0.0",
            sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1")
    print(f"[INFO] Connecting to: {publish}")
    socket.connect(publish)
    room = input('Room: ').strip().lower()
    while True:
        text = input('Text: ')
        print(f'{room} {text}')
        socket.send_string(f'{room} {text}')
