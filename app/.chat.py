# from flask import Flask;
# from flask_socketio import SocketIO, send

# # from flask_cors import cors_allowed_origins

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'YOU-SHALL-NOT-PASS'

# socketIo = SocketIO(app, cors_allowed_origins="*")

# app.debug = True
# app.host = 'localhost'

# @socketIo.on('message')
# def handleMessage(msg):
#     print(msg)
#     send(msg, broadcast=True)
#     return None

# if __name__ == '__main__':
#     socketIo.run(app)