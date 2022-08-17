from flask import jsonify, request


def list_files():
    file = open('local/projects/test.txt')
    str = file.readlines()
    return jsonify({"str": str})