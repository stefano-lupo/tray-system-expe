from core.config import API_PORT

from api import app

if __name__ == "__main__":
    app.run(port=API_PORT)