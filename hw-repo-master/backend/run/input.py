from run.running_users import running_users


def input(data): #TODO: 获取输入，并传递给对应用户的项目 / data: session, project, text

    session = data.session
    project = data.project #用不到？
    inputText = data.text

    currentThread = running_users[session].run_thread
    currentExecuteProcess = currentThread.execute_subprocess
    currentExecuteProcess.stdin.write(inputText)
    currentExecuteProcess.stdin.flush()