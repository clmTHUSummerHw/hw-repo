from typing import Dict
from unittest import result
from flask import jsonify, request
import os
from project.utils import get_root
from user.user_dict import user_dict
from db.models import User


def build_dir(root: str, dir: str) -> Dict:
    full = root + '/' + dir
    if os.path.isdir(full):
        children = []
        result = {'name': dir, 'folder': 1, 'files': children}
        children_names = os.listdir(full)
        for i in children_names:
            children.append(build_dir(full, i))
        return result
    else:
        return {'name': dir, 'folder': 0}


def list_files():
    if not request.is_json:
        return jsonify({'code': -1, 'files': []})

    session = request.json['session']
    project_name = request.json['project']

    if not isinstance(session, str) or not isinstance(project_name, str):
        return jsonify({'code': -1, 'files': []})

    code, root = get_root(session, project_name)

    if code == 1:
        return jsonify({'code': 1, 'files': []})

    if code == 2:
        return jsonify({'code': 2, 'files': []})

    out = []

    files = os.listdir(root)
    for i in files:
        out.append(build_dir(root, i))
    return jsonify({'code': 0, 'files': out})
