from core.config import API_PORT
from flask_cors import CORS as cors
from backend.api.routes import *

from backend.api import app

# from flask import Flask
# app = Flask(__name__)

if __name__ == "__main__":
    cors(app)
    app.run(port=API_PORT)
