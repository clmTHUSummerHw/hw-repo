from typing import Tuple
from user.user_dict import user_dict
from db.models import User


def get_root(session: str, project_name: str) -> Tuple[int, str]:
    if session not in user_dict:
        return 1, ''

    username = user_dict[session].username
    user = User.query.filter_by(username=username).first()
    project = user.projects.filter_by(name=project_name).first()

    if project is None:
        return 2, ''

    root = './project_storage/' + username + '/' + project_name
    return 0, root