from debug.debugging_projects import debugging_projects


def query_value(data):
    session = data['session']
    var = data['var']
    if not isinstance(session, str) or not isinstance(var, str):
        return

    debugging_project = debugging_projects[session]
    debug_thread = debugging_project.debug_thread
    debug_thread.input_queue.put('dump %s' % var)