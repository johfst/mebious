from flask import Flask

TESTING = True
DEBUG = True
FLASK_ENV = "development"
SECRET_KEY = ""

UPLOAD_FOLDER = "static/images"
MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 16 MB
