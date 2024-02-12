import zmq 
context = zmq.Context()

if __name__ == '__main__':
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://0.0.0.0:5556')
    while True:
        room = input('Room: ')
        text = input('Text: ')
        socket.send_string(f'{room} {text}')