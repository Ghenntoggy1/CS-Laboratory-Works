from flask import Flask
from flasgger import Swagger

from routes import router


def create_app():
    app = Flask(__name__)
    app.config["SWAGGER"] = {
        "title": "Vigenere Cipher Encryption/Decryption API",
        "description": "API for encrypting and decrypting text using the Vigenere cipher",
        "uiversion": 3
    }

    Swagger(app, template_file="docs/swagger_template.yml")

    app.register_blueprint(router)

    return app


if __name__ == '__main__':
    # try:
    #     port = int(sys.argv[1])
    # except Exception:
    #     port = 8081

    create_app().run()
