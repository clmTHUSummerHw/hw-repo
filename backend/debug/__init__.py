from ws.ws_helper import WsHelper

debug_api = WsHelper('/debug')

from debug.start import start
from debug.input import input
from debug.force_stop import force_stop
from debug.add_breakpoint import add_breakpoint
from debug.continue_running import continue_running
from debug.step_pass import step_pass
from debug.step_in import step_in
from debug.step_out import step_out
from debug.query_value import query_value

debug_api.on_event('start', start)
debug_api.on_event('input', input)
debug_api.on_event('force_stop', force_stop)
debug_api.on_event('add_breakpoint', add_breakpoint)
debug_api.on_event('continue_running', continue_running)
debug_api.on_event('step_pass', step_pass)
debug_api.on_event('step_in', step_in)
debug_api.on_event('step_out', step_out)
debug_api.on_event('query_value', query_value)