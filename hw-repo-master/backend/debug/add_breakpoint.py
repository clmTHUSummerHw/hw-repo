from debug.debugging_projects import debugging_projects


def add_breakpoint(data):
    session = data['session']
    file = data['file']
    line = data['line']
    if not isinstance(session, str) or not isinstance(file, str) or not isinstance(line, int):
        return

    if file.endswith('.java'):
        file = file[:-5]

    debugging_project = debugging_projects[session]
    debug_thread = debugging_project.debug_thread
    debug_thread.input_queue.put('stop at %s:%d' % file % line)