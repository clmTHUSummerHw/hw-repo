from flask import Flask
from user import user_api
from project import project_api
from test_flask import test


app = Flask(__name__)

app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(project_api, url_prefix='/project')
app.add_url_rule('/test', view_func=test, methods=['POST'])


if __name__ == '__main__':
   app.debug = True
   print(app.route)
   app.run()