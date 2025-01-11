from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from main import get_highlights
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

DEBUG = os.getenv("FLASK_ENV", "DEVELOPMENT")


@app.route('/list/highlights', methods=['POST'])
def custom_endpoint():
    try:
        # Parse JSON data from the request body
        data = request.get_json()

        email = data.get('email', os.getenv('EMAIL', 'No email provided'))
        password = data.get('password', os.getenv('PASSWORD', 'No password provided'))
        username = data.get('username', os.getenv('TW_USERNAME', 'No username provided'))

        response = get_highlights(email, username, password)
        status = 200 if response.get("code") == 1 else 400 if response.get("code") == 0 else 500
        return jsonify(response), status
    except Exception as err:
        print("Caught exception to: ")
        print(err)
        return jsonify({"code": -1, "message": err}), 500


if __name__ == '__main__':
    app.run(debug=(DEBUG == "DEVELOPMENT"))
