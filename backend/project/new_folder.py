import os
import re
from typing import List
from flask import request, jsonify
from project.utils import split_path, get_root, check_and_make_dirs


file_name_re = re.compile(r'([/\\][^/\\:\*\?"<>\|\f\n\r\t\v]*[^/\\:\*\?"<>\|\f\n\r\t\v\.])+')


def new_folder():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    file_full = request.json['name']

    if not isinstance(session, str) or not isinstance(project_name, str) or not isinstance(file_full, str):
        return jsonify({'code': -1})

    if not file_name_re.match(file_full):
        return jsonify({'code': 3})

    paths = split_path(file_full)
    file_name = paths[len(paths) - 1]
    paths.pop()

    code, root = get_root(session, project_name)

    if code != 0:
        return jsonify({'code': code})

    if os.path.exists(root + file_full):
        return jsonify({'code': 4})

    if not check_and_make_dirs(root, paths):
        return jsonify({'code': 3})

    try:
        os.makedirs(root + '/' + file_full)
    except Exception:
        return jsonify({'code': -1})

    return jsonify({'code': 0})
