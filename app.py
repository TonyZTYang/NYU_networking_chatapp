from flask import Flask, send_from_directory
from flask_restful import Resource, Api,reqparse
from os import path

app = Flask(__name__)

api = Api(app)
parser = reqparse.RequestParser()

pwd = path.dirname(path.realpath(__file__))
users = {"test": 1}
rooms = {
    "Public": [],
    1: ["test"]
}

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
        parser.add_argument("username",type=str)
        username = parser.parse_args()["username"]
        if username in users.keys():
            return {"status": 0}
        else:
            users[username] = "Public"
            rooms["Public"].append(username)
            print("new user " + username)
            return {"status": 1}

class Logout(Resource):
    def post(self):
        parser.add_argument("username",type=str)
        username = parser.parse_args()["username"]
        if username in users.keys():
            room = users.pop(username)
            rooms[room].remove(username)
            if ((room != "Public") and (rooms[room] == [])):
                del rooms[room]
            return {"status": 1}

api.add_resource(Login,"/login")
api.add_resource(Logout,"/logout")

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, True)