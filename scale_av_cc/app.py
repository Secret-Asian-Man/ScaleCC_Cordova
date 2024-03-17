import json
import logging
import zmq
from pathlib import Path
from flask import Flask
from .constants import REQUEST_ADDRESS

logging.getLogger().setLevel(logging.INFO)
logging.info("Logging system initialized!")

LOGGER = logging.getLogger(__name__)

ROOM_DATA_OBJECTS = {}

STATIC_FILES_FOLDER = Path(__file__).parent.parent / 'www'
app = Flask(__name__, static_url_path='', static_folder=STATIC_FILES_FOLDER)
app.config.from_prefixed_env()

context = zmq.Context()

@app.route('/')
def index():
    ''' HTML route handling index.html -> / translation '''
    return app.send_static_file('index.html')

@app.route('/room/<room_id>/latest', methods=['GET'])
def get_room_latest(room_id):
    socket = context.socket(zmq.REQ)
    try:
        socket.setsockopt(zmq.CONNECT_TIMEOUT, 100)
        request = REQUEST_ADDRESS.replace("0.0.0.0", "127.0.0.1")
        LOGGER.info("Connecting to: %s", request)
        socket.connect(request)
        socket.send_string(room_id)
        latest = socket.recv_string()
    except zmq.ZMQError as exc:
        LOGGER.warn("Error occurred: %s", str(exc))
        latest = str(exc)
    finally:
        socket.close()
    return json.dumps(
        {
            'room': room_id,
            'text': latest
        }
    )
