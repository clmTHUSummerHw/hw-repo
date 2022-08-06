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


if __name__ == '__main__':
   app.run()