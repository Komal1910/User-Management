from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("one.html")

@app.route("/home/<name>")
def home(name):
    return render_template("one.html", n = name)

@app.route("/home/<name>/<int:m1>/<int:m2>/<int:m3>/")
def marks(name,m1,m2,m3):
    data = {
        "name":name,
        "science":m1,
        "mathe":m2,
        "english":m3
    }
    return render_template("one.html",data = data)


app.run(host="localhost")
