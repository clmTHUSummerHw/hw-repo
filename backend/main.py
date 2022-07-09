from flask import Flask
from user import user_api
from project import project_api


app = Flask(__name__)

app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(project_api, url_prefix='/project')


if __name__ == '__main__':
   app.run()