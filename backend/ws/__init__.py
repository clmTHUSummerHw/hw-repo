from flask_socketio import SocketIO
from ws.connect_ws import connect_ws
from ws.disconnect_ws import disconnect_ws
from run import run_api
from debug import debug_api


ws = SocketIO()

ws.on_event('connect_ws', connect_ws)
ws.on_event('disconnect_ws', disconnect_ws)

run_api.init_ws(ws)
debug_api.init_ws(ws)