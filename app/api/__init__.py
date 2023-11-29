from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS

api = Blueprint('api', __name__, url_prefix='/api')
CORS(api) # CORS only to api blueprint
@api.route('/test')
def test():
    return 'this is a test'

app = Flask(__name__)
CORS(app) #apply CORS to entire app

# @app.route('/api/users', methods=['POST', 'OPTIONS'])
# def handle_users():
#     if request.method == 'OPTIONS':
#         response = jsonify({'message': 'Preflight request successful'})
#         response.headers.add('Access-Control-Allow-Methods', 'POST')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         return response
#     elif request.method == 'POST':
#         # Your POST request handling logic goes here
#         return jsonify({'message': 'POST request successful'})

if __name__ == '__main__':
    app.run(debug=True)


from app.api import users, errors,  routes