from debug.debugging_projects import debugging_projects


def input(data):
    session = data['session']
    text = data['text']
    if not isinstance(session, str) or not isinstance(text, str):
        return

    debugging_project = debugging_projects[session]
    run_thread = debugging_project.run_thread
    run_process = run_thread.execute_subprocess
    run_process.stdin.write(text)
    run_process.stdin.flush()