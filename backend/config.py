SQL_HOST = '127.0.0.1'
SQL_PORT = '3306'
SQL_DATABASE = 'flask'
SQL_USERNAME = 'flask'
SQL_PASSWORD = '123456'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=SQL_USERNAME,password=SQL_PASSWORD, host=SQL_HOST,port=SQL_PORT, db=SQL_DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True