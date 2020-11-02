from flask import Flask

app = Flask(__name__)


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World!</h1>"

@app.route("/decline")
def decline():
    return "<h3>Hello World!</h3>"

@app.route("/underline")
def underline():
    return "<h1><u>Hello World!</u></h1>"

if __name__ == "__main__" :
    app.run(host='0.0.0.0',port=8000)