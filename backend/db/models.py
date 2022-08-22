from email.policy import default
from db import db
import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(64))
    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return '<User %r>' % self.username

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship('User', backref=db.backref('projects', lazy='dynamic'))

    def __init__(self, name, user) -> None:
        super().__init__()
        self.name = name
        self.user = user

    def __repr__(self) -> str:
        return '<Project %r>' % self.name

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, default=datetime.datetime.now)

    # 0-建立项目；1-新建文件；2-新建文件夹；3-移除文件；4-移除文件夹；5-上传文件；6-下载文件；7-运行；8-调试；
    # 9-添加依赖；10-移除依赖；11-打包；
    code = db.Column(db.Integer)

    # code为1或3或5或6时：文件名
    # code为2或4时：文件夹名
    # code为9或10时：依赖文件名
    # 其他code：空字符串
    extra_data = db.Column(db.String(65536))
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))

    # 获得项目对象（假设名为obj）时，使用obj.log即可查看与其相关的日志
    project = db.relationship('Project', backref=db.backref('log', lazy='dynamic'))

    # 注意，此处project要传一个Project对象，code类型为int，extra_data类型为string
    def __init__(self, code, extra_data, project) -> None:
        super().__init__()
        self.code = code
        self.extra_data = extra_data
        self.project = project