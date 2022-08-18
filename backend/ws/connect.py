from flask_socketio import join_room


def connect(data):
    session = data['session']
    join_room(session)