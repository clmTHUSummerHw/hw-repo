from main import app
import config
from db import db, models

app.config.from_object(config)
db.init_app(app)
app.app_context().push()

with app.app_context():
    db.create_all()