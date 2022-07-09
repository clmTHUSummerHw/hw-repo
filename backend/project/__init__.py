from flask import Blueprint
from list_files import list_files
from new_file import new_file
from delete_file import delete_file
from new_folder import new_folder
from delete_folder import delete_folder
from upload_file import upload_file
from download_file import download_file


project_api = Blueprint('project', __name__)

project_api.add_url_rule('/', 'list-files', list_files, methods=['POST'])
project_api.add_url_rule('/', 'new-file', new_file, methods=['POST'])
project_api.add_url_rule('/', 'delete-file', delete_file, methods=['POST'])
project_api.add_url_rule('/', 'new-folder', new_folder, methods=['POST'])
project_api.add_url_rule('/', 'delete-folder', delete_folder, methods=['POST'])
project_api.add_url_rule('/', 'upload-file', upload_file, methods=['POST'])
project_api.add_url_rule('/', 'download-file', download_file, methods=['POST'])