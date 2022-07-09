from flask import Blueprint
from user.register import register
from user.login import login
from user.logout import logout
from user.list_projects import list_projects
from user.new_project import new_project
from user.delete_project import delete_project


user_api = Blueprint('user', __name__)

user_api.add_url_rule('/register', view_func=register, methods=['POST'])
user_api.add_url_rule('/login', view_func=login, methods=['POST'])
user_api.add_url_rule('/logout', view_func=logout, methods=['POST'])
user_api.add_url_rule('/list-projects', view_func=list_projects, methods=['POST'])
user_api.add_url_rule('/new-project', view_func=new_project, methods=['POST'])
user_api.add_url_rule('/delete-project', view_func=delete_project, methods=['POST'])
