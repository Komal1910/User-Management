from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    return "Hello world"

@app.route("/home/")
def home():
    return "<h1 style='color:red'>Welcome to our homepage</h1>"

@app.route("/home/index/")
def home1():
    return "<h1 style='color:pink'>Flask Project</h1>"

app.run(host="localhost", port=80, debug=True)
