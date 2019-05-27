from flask import Flask

app = Flask(__name__, static_folder='static')
# app = Flask(__name__)

from backend.api.routes import *
