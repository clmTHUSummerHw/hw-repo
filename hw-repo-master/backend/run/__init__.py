from ws.ws_helper import WsHelper

run_api = WsHelper('/run')

from run.start import start
from run.input import input
from run.force_stop import force_stop

run_api.on_event('start', start)
run_api.on_event('input', input)
run_api.on_event('force_stop', force_stop)
