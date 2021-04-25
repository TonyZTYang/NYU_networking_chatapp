from flask import Flask, send_from_directory
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from os import path
from datetime import datetime
import json

app = Flask(__name__)

api = Api(app)
# parser = reqparse.RequestParser()

users = {"test": "1"}
rooms = {
    "Public": [],
    "1": ["test"]
}
# messages = {
#     "Public": [],
#     "1": {0: {"time": "2021.04.25 00:00:00", "name": "test", "text": "hey there"}}
# }
messages = {
    "Public": [],
    "1": [[ "2021.04.25 00:00:00", "test",  "hey there"], ["asf", "asdf", "asdf"]]
}

pwd = path.dirname(path.realpath(__file__))
user_room_change = 0
message_change = {
    "Public": 0,
    "1": 1
}
next_room = 2

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
                del message_change[room]
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
            # room = users[username]
            # print(room)
            # room_member = rooms[room]
            # room.remove(username)
            return {
                "changed": 1,
                "server_urc": user_room_change,
                "users": users
            }
class MakeUserRoomChange(Resource):
    def post(self):
        global user_room_change
        global next_room
        parser = reqparse.RequestParser()
        parser.add_argument("myName", type=str)
        parser.add_argument("otherName",type=str)
        myId = parser.parse_args()["myName"]
        otherId = parser.parse_args()["otherName"]
        myRoom = users[myId]
        otherRoom = users[otherId]
        user_room_change += 1
        if myRoom == otherRoom:
            new_room = str(next_room)
            next_room += 1
            rooms[new_room] = [myId, otherId]
            message_change[new_room] = 0
            messages[new_room] = []
            users[myId] = new_room
            users[otherId] = new_room
            rooms[myRoom].remove(myId)
            rooms[myRoom].remove(otherId)
            if ((myRoom != "Public") and (rooms[myRoom] == [])):
                del rooms[myRoom]
        else:
            users[myId] = otherRoom
            rooms[myRoom].remove(myId)
            rooms[otherRoom].append(myId)
            if ((myRoom != "Public") and (rooms[myRoom] == [])):
                del rooms[myRoom]
        return {"status": 1}

class GetMessageChange(Resource):
    def post(self):
        global message_change
        parser = reqparse.RequestParser()
        parser.add_argument("messageChange", type=int)
        parser.add_argument("username",type=str)
        client_msgc = parser.parse_args()["messageChange"]
        username = parser.parse_args()["username"]
        if username == '':
            return {"changed":0}
        room = users[username]
        if client_msgc == message_change[room]:
            return {"changed":0}
        else:      
            return {
                "changed": 1,
                "messageChange": message_change[room],
                "messages": messages[room]
            }


api.add_resource(Login,"/login")
api.add_resource(Logout,"/logout")
api.add_resource(GetUserRoomChange, "/getUserRoomChange")
api.add_resource(MakeUserRoomChange, "/makeUserRoomChange")
api.add_resource(GetMessageChange, "/getMessageChange")

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, True)