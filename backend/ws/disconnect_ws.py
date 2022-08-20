from flask_socketio import leave_room


def disconnect_ws(data):
    session = data['session']
    leave_room(session)