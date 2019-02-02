import os
import binascii

CSRF_ENABLED = True
SECRET_KEY = binascii.hexlify(os.urandom(24)).decode()

DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = '199892.lw'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'app_hbuhelp'
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI