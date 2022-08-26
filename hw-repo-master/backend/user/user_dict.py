
from typing import Dict


class UserInfo():
    username = str

    def __init__(self, username) -> None:
        self.username = username



user_dict: Dict[str, UserInfo] = {}  # session: userinfo(class UserInfo)

def joindict(session = str, username = str):
    user_dict[session] = UserInfo(username)

