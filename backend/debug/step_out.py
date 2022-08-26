from debug.debugging_projects import debugging_projects


def step_out(data):
    session = data['session']
    if not isinstance(session, str):
        return

    debugging_project = debugging_projects[session]
    debug_thread = debugging_project.debug_thread
    debug_thread.input_queue.put('step up')