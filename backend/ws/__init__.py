from flask_socketio import SocketIO
from ws.connect import connect
from ws.disconnect import disconnect


ws = SocketIO()

ws.on_event('connect', connect)
ws.on_event('disconnect', disconnect)