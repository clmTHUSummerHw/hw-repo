from flask_socketio import leave_room


def disconnect(data):
    session = data['session']
    leave_room(session)