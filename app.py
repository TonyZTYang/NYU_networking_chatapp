from flask import Flask, send_from_directory
from flask_restful import Resource, Api,reqparse
from os import path
from datetime import datetime

app = Flask(__name__)

api = Api(app)
# parser = reqparse.RequestParser()

users = {"test": 1}
rooms = {
    "Public": [],
    1: ["test"]
}

pwd = path.dirname(path.realpath(__file__))
user_room_change = 0

# return the full app
@app.route('/', methods=['GET'])
def index_get():
    return send_from_directory(pwd, "vue_app/index.html")
        
@app.route('/vue.js', methods=['GET'])
def vuejs_get():
    return send_from_directory(pwd, "vue_app/vue.js")

@app.route('/script.js', methods=['GET'])
def scriptjs_get():
    return send_from_directory(pwd,  "vue_app/script.js")

@app.route('/bootstrap.css', methods=['GET'])
def bootstrapcss_get():
    return send_from_directory(pwd, "vue_app/bootstrap.css")

@app.route('/style.css', methods=['GET'])
def stylecss_get():
    return send_from_directory(pwd, "vue_app/style.css")

class Login(Resource):
    def post(self):
        global user_room_change
        parser = reqparse.RequestParser()
        parser.add_argument("username",type=str)
        username = parser.parse_args()["username"]
        if username in users.keys():
            return {"status": 0}
        else:
            users[username] = "Public"
            rooms["Public"].append(username)
            user_room_change += 1
            print("new user " + username)
            return {"status": 1}

class Logout(Resource):
    def post(self):
        global user_room_change
        parser = reqparse.RequestParser()
        parser.add_argument("username",type=str)
        username = parser.parse_args()["username"]
        if username in users.keys():
            room = users.pop(username)
            rooms[room].remove(username)
            user_room_change += 1
            if ((room != "Public") and (rooms[room] == [])):
                del rooms[room]
            return {"status": 1}

class GetUserRoomChange(Resource):
    def post(self):
        global user_room_change
        parser = reqparse.RequestParser()
        parser.add_argument("user_room_change", type=int)
        parser.add_argument("username",type=str)
        client_urc = parser.parse_args()["user_room_change"]
        username = parser.parse_args()["username"]
        if client_urc == user_room_change:
            return {"changed": 0}
        else:
            print(username)
            print(client_urc)
            # room = users[username]
            # print(room)
            # room_member = rooms[room]
            # room.remove(username)
            return {
                "changed": 1,
                "server_urc": user_room_change,
                "users": users,
                "room": {}
            }

api.add_resource(Login,"/login")
api.add_resource(Logout,"/logout")
api.add_resource(GetUserRoomChange, "/getUserRoomChange")

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, True)