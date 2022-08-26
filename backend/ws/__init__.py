from flask_socketio import SocketIO
from run import run_api
from debug import debug_api


ws = SocketIO()

run_api.init_ws(ws)
debug_api.init_ws(ws)