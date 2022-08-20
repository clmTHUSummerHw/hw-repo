from flask_socketio import join_room, emit


def connect(data):
    session = data['session']
    join_room(session)
    emit('accept_connection', {})