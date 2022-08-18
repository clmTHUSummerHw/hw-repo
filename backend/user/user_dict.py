
class UserInfo():
    username = str

    def __init__(self, username) -> None:
        username = username
        pass


user_dict = {}  # session: userinfo(class UserInfo)

def joindict(session = str, username = str):
    user_dict[session] = UserInfo(username)

