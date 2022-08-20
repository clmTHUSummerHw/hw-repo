from flask_socketio import join_room, emit


def connect_ws(data):
    session = data['session']
    join_room(session)
    emit('accept_connection', {})