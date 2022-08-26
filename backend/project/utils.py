import os
from typing import List, Tuple
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


def get_dependency_root(session: str, project_name: str) -> Tuple[int, str]:
    if session not in user_dict:
        return 1, ''

    username = user_dict[session].username
    user = User.query.filter_by(username=username).first()
    project = user.projects.filter_by(name=project_name).first()

    if project is None:
        return 2, ''

    root = './project_storage/' + username + '/' + project_name + '@dependency'
    if not os.path.exists(root):
        os.makedirs(root)
    return 0, root


def split_path(full: str) -> List[str]:
    out:List[str] = []
    path, file = os.path.split(full)
    if path != '' and path != '/':
        out = split_path(path)
    out.append(file)
    return out

def check_and_make_dirs(current_dir: str, path: List[str]) -> bool:
    if not os.path.exists(current_dir):
        os.makedirs(current_dir)

    if not os.path.isdir(current_dir):
        return False

    if len(path) == 0:
        return True

    newPath: List[str] = []

    for i in range(1, len(path)):
        newPath.append(path[i])

    return check_and_make_dirs(current_dir + '/' + path[0], newPath)