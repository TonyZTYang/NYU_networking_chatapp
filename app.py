from flask import Flask, send_from_directory
from os import path

app = Flask(__name__)

pwd = path.dirname(path.realpath(__file__))

# return the full app
@app.route('/', methods=['GET'])
def index_get():
    return send_from_directory(pwd, "index.html")
        
@app.route('/vue.js', methods=['GET'])
def vuejs_get():
    return send_from_directory(pwd, "vue.js")

@app.route('/main.js', methods=['GET'])
def mainjs_get():
    return send_from_directory(pwd,  "main.js")

@app.route('/bootstrap.css', methods=['GET'])
def bootstrapcss_get():
    return send_from_directory(pwd, "bootstrap.css")



if __name__ == "__main__":
    app.run("127.0.0.1", 5000, True)