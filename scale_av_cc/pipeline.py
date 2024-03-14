import zmq
import platform
import sys

context = zmq.Context()

if __name__ == "__main__":
    node = platform.node().replace("-", "_").replace(" ", "_")
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://0.0.0.0:7500')
    for line in sys.stdin:
        socket.send_string(f"{node} {line}")