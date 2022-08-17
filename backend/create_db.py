from main import app
import config
from db import db, models
import os

app.config.from_object(config)
db.init_app(app)
app.app_context().push()

with app.app_context():
    db.create_all()

if not os.path.isdir('local'):
    os.mkdir('local')

if not os.path.isdir('local/projects'):
    os.mkdir('projects')