from flask import Blueprint
from project.list_files import list_files
from project.new_file import new_file
from project.delete_file import delete_file
from project.new_folder import new_folder
from project.delete_folder import delete_folder
from project.upload_file import upload_file
from project.download_file import download_file
from project.add_dependency import add_dependency
from project.remove_dependency import remove_dependency
from project.list_dependencies import list_dependencies


project_api = Blueprint('project', __name__)

project_api.add_url_rule('/list-files', view_func=list_files, methods=['POST'])
project_api.add_url_rule('/new-file', view_func=new_file, methods=['POST'])
project_api.add_url_rule('/delete-file', view_func=delete_file, methods=['POST'])
project_api.add_url_rule('/new-folder', view_func=new_folder, methods=['POST'])
project_api.add_url_rule('/delete-folder', view_func=delete_folder, methods=['POST'])
project_api.add_url_rule('/upload-file', view_func=upload_file, methods=['POST'])
project_api.add_url_rule('/download-file', view_func=download_file, methods=['POST'])
project_api.add_url_rule('/add-dependency', view_func=add_dependency, methods=['POST'])
project_api.add_url_rule('/remove-dependency', view_func=remove_dependency, methods=['POST'])
project_api.add_url_rule('/list-dependencies', view_func=list_dependencies, methods=['POST'])