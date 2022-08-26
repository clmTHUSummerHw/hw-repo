import base64
import os
import re
from flask import request, jsonify
from project.utils import add_log_with_session, check_and_make_dirs, get_root, split_path


file_name_re = re.compile(r'([/\\][^/\\:\*\?"<>\|\f\n\r\t\v]*[^/\\:\*\?"<>\|\f\n\r\t\v\.])+')


def upload_file():
    if not request.is_json:
        return jsonify({'code': -1})

    session = request.json['session']
    project_name = request.json['project']
    file_full = request.json['name']
    file_base64 = request.json['file']

    if not isinstance(session, str) \
        or not isinstance(project_name, str) \
        or not isinstance(file_full, str) \
        or not isinstance(file_base64, str):
        return jsonify({'code': -1})

    if not file_name_re.match(file_full):
        return jsonify({'code': 3})

    file_content = ''
    try:
        file_content = base64.b64decode(file_base64).decode()
    except Exception:
        return jsonify({'code': 5})

    paths = split_path(file_full)
    file_name = paths[len(paths) - 1]
    paths.pop()

    code, root = get_root(session, project_name)

    if code != 0:
        return jsonify({'code': code})

    if os.path.isdir(root + file_full):
        return jsonify({'code': 4})

    if not check_and_make_dirs(root, paths):
        return jsonify({'code': 3})

    try:
        f = open(root + '/' + file_full, 'w', encoding='utf-8')
        f.write(file_content)
        f.close()
    except Exception:
        return jsonify({'code': -1})

    add_log_with_session(session, project_name, 5, file_full)
    return jsonify({'code': 0})