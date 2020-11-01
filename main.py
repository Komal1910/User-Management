from flask import Flask, render_template, request, make_response, session, redirect, url_for
import pymysql as sql
import smtplib, ssl
from email.mime.text import MIMEText
#from email.MIMEMultipart import MIMEMultipart
from random import randint
import os

app = Flask(__name__)
app.secret_key = "oihbauyiegbgycgabiuhdsjvjgasb"

db = sql.connect(host="localhost", port = 3307, user="root", password="root", database="test")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login_user", methods=["POST","GET"])
def login_user():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")        
        if email:
            if password:
                cursor = db.cursor()
                cmd = "select * from users where email=%s and password=%s"
                args=(email, password)
                cursor.execute(cmd, args)
                data = cursor.fetchone()
                if data:
                    res = make_response(redirect (url_for("dashboard")))
                    res.set_cookie('user_email', data[3])
                    return res
                else:                       
                    error = "Invalid email or password"
                    return render_template("login.html",error=error)    
            else:
                error = "Invalid password"
                return render_template("login.html",error = error)
        else:
                error = "Invalid email"
                return render_template("login.html",error = error)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup_user", methods=["POST","GET"])
def signup_user():
    if request.method == "POST":        
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        password = request.form.get("password")   
        gender = request.form.get("gender")
        mobile = request.form.get("mobile")
        username = email.split("@")[0]    
        if email and password:
            cursor = db.cursor()
            cmd = "select * from users where email=%s"
            args=(email,)
            cursor.execute(cmd, args)
            data = cursor.fetchone()
            if data:
                error = "Email already registered"
                return render_template("signup.html", error=error)
            else:
                cmd = "insert into users (fname, lname, email, password, gender, mobile, username) values (%s, %s, %s, %s, %s, %s, %s)"
                args = (fname, lname, email, password, gender, mobile, username)
                cursor.execute(cmd, args)
                db.commit()
                return redirect (url_for("login"))           
        else:
            error = "Invalid Email or password"
            return render_template("signup.html",error=error)
    else:
        render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    user_email = request.cookies.get('user_email')
    if user_email: 
        return render_template("dashboard.html")
    else: 
        return redirect (url_for("login"))

@app.route("/profile")
def profile():
    user_email = request.cookies.get('user_email')
    if user_email: 
        cursor = db.cursor()
        cmd = "select * from users where email=%s"
        args = (user_email,)
        cursor.execute(cmd, args)
        data = cursor.fetchall()
        data = list(list(data)[0])
        user_data = {
            "fname": data[1],
            "lname": data[2],
            "username": data[7],
            "email": data[3],
            "gender": data[5],
            "mobile": data[6],
        }
        return render_template("profile.html", data=user_data)
    else: 
        return redirect (url_for("login"))

@app.route("/projects")
def projects():
    user_email = request.cookies.get('user_email')
    if user_email: 
        cursor = db.cursor()
        cmd = "select * from projects p inner join project_tasks_mapping ptm on p.id=ptm.project_id;"
        cursor.execute(cmd)
        data = cursor.fetchall()
        data = list(data)
        projects_data=[]
        for project in data:
            project=list(project)
            projects_data.append({
                "name": project[1],
                "budget": project[2],
                "tasks_status": {
                    project[5]: project[6]
                }
            })
        return render_template("projects.html", data=projects_data)
    else: 
        return redirect (url_for("login"))

@app.route("/add_project")
def add_project():
    user_email = request.cookies.get('user_email')
    if user_email: 
        return render_template("add_projects.html")
    else: 
        return redirect (url_for("login"))

@app.route("/add_project_submit", methods=["POST","GET"])
def add_project_submit():
    user_email = request.cookies.get('user_email')
    if user_email: 
        if request.method == "GET":
            return render_template("add_projects.html")
        elif request.method == "POST":
            name = request.form.get("name")
            budget = request.form.get("budget")
            task = request.form.get("task")
            cursor = db.cursor()
            cmd = "insert into projects (name, budget) values (%s, %s)"
            args = (name, budget)
            result = cursor.execute(cmd, args)
            db.commit()
            project_id = cursor.lastrowid
            cmd = "insert into project_tasks_mapping (project_id, task) values (%s, %s)"
            args = (project_id, task)
            cursor.execute(cmd, args)
            db.commit()
            return redirect (url_for("projects"))          
        else:
            render_template("signup.html")
    else: 
        return redirect (url_for("login"))

@app.route("/employees")
def employees():
    return render_template("employees.html")

@app.route("/logout")
def logout():
    res = make_response(redirect (url_for("login")))
    res.delete_cookie('user_email')
    return res

app.run(host="localhost", port=8080, debug=True)
 