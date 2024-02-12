import json
from pathlib import Path
from flask import Flask
from .data import RandomData
from .zmq import ZmqData
ROOM_DATA_OBJECTS = {}

STATIC_FILES_FOLDER = Path(__file__).parent.parent / 'www'
app = Flask(__name__, static_url_path='', static_folder=STATIC_FILES_FOLDER)
app.config.from_prefixed_env()

@app.route('/')
def index():
    ''' HTML route handling index.html -> / translation '''
    return app.send_static_file('index.html')

@app.route('/room/<room_id>/latest', methods=['GET'])
def get_room_latest(room_id):
    room_data = get_room_handler(room_id)
    return json.dumps(
        room_data.get_latest()
    )

def get_room_handler(room_id):
    ''' Get the room handler for a given room id '''
    ROOM_DATA_OBJECTS[room_id] = ROOM_DATA_OBJECTS.get(room_id, get_new_handler(room_id))
    return ROOM_DATA_OBJECTS[room_id]

def get_new_handler(room_id):
    return RandomData(room_id) if app.config.get('HANDLER', None) == 'RandomData' else ZmqData(room_id)