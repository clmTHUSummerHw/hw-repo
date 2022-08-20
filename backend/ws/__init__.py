from flask_socketio import SocketIO
from ws.connect import connect
from ws.disconnect import disconnect
from run import run_api
from debug import debug_api


ws = SocketIO(cors_allowed_origins='*')

ws.on_event('connect_ws', connect)
ws.on_event('disconnect_ws', disconnect)

run_api.init_ws(ws)
debug_api.init_ws(ws)