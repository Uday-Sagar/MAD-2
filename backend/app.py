from website import create_app
from flask_cors import CORS


if __name__ == '__main__':
    app = create_app()
    CORS(app, supports_credentials=True)
    app.run(host="127.0.0.1", debug=True, port=7644)