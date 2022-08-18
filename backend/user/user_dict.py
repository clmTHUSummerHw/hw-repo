
class UserInfo():
    username = str

    def __init__(self, username) -> None:
        username = username
        pass


UserDict = {}  # session: userinfo(class UserInfo)

def joindict(session = str, username = str):
    UserDict[session] = UserInfo(username)

