from flask import Flask
from user import user_api
from project import project_api
import config
from db import db, models


app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)

app.register_blueprint(user_api, url_prefix='/user')
app.register_blueprint(project_api, url_prefix='/project')
app.add_url_rule('/test', view_func=test, methods=['POST'])


if __name__ == '__main__':
   app.debug = True
   print(app.route)
   app.run()