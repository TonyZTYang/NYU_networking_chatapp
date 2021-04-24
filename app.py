from flask import Flask, send_from_directory
from os import path

app = Flask(__name__)

pwd = path.dirname(path.realpath(__file__))

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



if __name__ == "__main__":
    app.run("127.0.0.1", 5000, True)