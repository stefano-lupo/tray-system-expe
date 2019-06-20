##################################
# Runs the backend API
##################################

from core.config import API_PORT, API_HOST
from flask_cors import CORS as cors

from backend.api import app

if __name__ == "__main__":
    cors(app)
    app.run(port=API_PORT, host=API_HOST)

