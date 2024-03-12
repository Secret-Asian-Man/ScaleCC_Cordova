import json
import logging
import threading
from .constants import LOCAL_ADDRESS

import zmq

logging.getLogger().setLevel(logging.INFO)
logging.info("Logging system initialized!")

LOGGER = logging.getLogger(__name__)

RUNNING = True
LATEST = {}

context = zmq.Context()


def run():
    """ Run the thread accepting connections """
    LOGGER.info("Binding to %s", LOCAL_ADDRESS)
    socket = context.socket(zmq.REP)
    socket.bind(LOCAL_ADDRESS)
    while RUNNING:
        message = socket.recv().decode()
        LOGGER.debug("Received message: %s", message)
        socket.send_string(LATEST.get(message, "No cations available."))


def loop(rooms):
    """ Run the main loop """
    global RUNNING
    global LATEST
    try:
        socket = context.socket(zmq.SUB)
        while True:
            for room in rooms:
                uri = room.get("uri", "--unknown--")
                name = room.get("room", "--unknown--")
                try:
                    logging.info("Subscribing to '%s' from '%s'", uri, name)
                    socket.setsockopt_string(zmq.SUBSCRIBE, name)
                    socket.connect(uri)
                except zmq.ZMQError:
                    logging.warning("Failed to subscribe '%s' from '%s'", uri, name)

            latest = socket.recv_string()
            room, text = latest.split(" ", 1)
            LATEST[room] = text
    finally:
        RUNNING = False


def main():
    """ Main function. Hi Lewis!!! """
    with open("rooms.json", "r") as file_handle:
        rooms = json.load(file_handle)
    thread = threading.Thread(target=run)
    thread.start()
    # Build a socket subscribed to all channels
    loop(rooms)





if __name__ == "__main__":
    main()