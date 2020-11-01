from flask import Flask, render_template, request, make_response, session, redirect, url_for
import pymysql as sql
import smtplib, ssl
from email.mime.text import MIMEText
#from email.MIMEMultipart import MIMEMultipart
from random import randint
import os

app = Flask(__name__)
app.secret_key = "oihbauyiegbgycgabiuhdsjvjgasb"

@app.route("/")
def login():
    # if request.cookies.get("islogin"):
    #     return render_template("afterlogin.html")
    return render_template("login.html")

@app.route("/login_user", methods=["POST","GET"])
def login_user():   
    # to be removed -- temporary code
    #return redirect (url_for("dashboard"))
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")        
        if email:
            if password:
                # to be removed -- temporary code
                # return redirect (url_for("dashboard"))
                try:
                    db = sql.connect(host="localhost", port = 3306, user="root", password="", database="komal")
                except Exception as e:
                    print(e)
                    return render_template("login.html")
                else:
                    cursor = db.cursor()
                    cmd = "select * from user where email='{email}' and password='{password}'"
                    cursor.execute(cmd)
                    data = cursor.fetchone()
                    if data:
                        username = data[6]
                        #resp = make_response(render_template("afterlogin.html"))
                        #resp.set_cookie("email",email)
                        #resp.set_cookie("islogin","true")
                        #return resp
                        session['email'] = email
                        session["islogin"] = "True"
                        return render_template("dashboard.html",user=username)
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
        print("Hello")       
        if email and password:
             try:
                db = sql.connect(host="localhost", port=3306, user="root", password="", database="komal")
             except Exception as e:
                print(e)
                return render_template("signup.html")
             else:
                    cursor = db.cursor()
                    cmd = "select * from spacedecor where email='{email}'"
                    cursor.execute(cmd)
                    data = cursor.fetchone()
                    print("---------------------", data)
                    if data:
                        error = "Email already registered"
                        return render_template("signup.html",error=error)
                    else:
                        if len(password)>=8:
                            s = 0
                            l = 0
                            u = 0
                            n = 0
                            for i in password:
                                special = "".join(["@","&","$","*","#","%","!"])
                                if i in special:
                                    s += 1 
                                if i.islower():
                                    l += 1
                                if i.isupper():
                                    u += 1
                                if i.isdigit():
                                    n += 1
                            if s>=1 and l>=1 and u>=1 and n>=1:
                                print("Inser query next")                                                                
                                cmd = "insert into spacedecor values ('{fname}','{lname}','{email}','{password}','{gender}', '{mobile}','{username}')"
                                cursor.execute(cmd)
                                print("Successful")
                                db.commit()
                                print("Hi")
                                redirect (url_for("login"))
                            else:
                                error = "Incorrect Password"
                                return render_template("signup.html",error=error)
                        else:
                            error = "Incorrect Password"
                            return render_template("signup.html",error=error)            
        else:
            error = "Invalid Email or password"
            return render_template("signup.html",error=error)
    else:
        render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    # get this data from the database and pass to template in the below format
    cursor = db.cursor()
    cmd = "select * from spacedecor where email='{email}'"
    cursor.execute(cmd)
    d = cursor.fetchall()
    user_data = {
        "fname": "Komal",
        "lname": "Hazari",
        "username": "komal1505",
        "email": "komal1505@gmail.com",
        "gender": "Female",
        "mobile": "+919999999999",
    }
    return render_template("profile.html", data=user_data)

@app.route("/projects")
def projects():
    # get this data from the database and pass to template in the below format
    projects_data = [
        {
            "name": "EtonX",
            "budget": 100,
            "tasks_status": {
                "Requirement Gathering": 1,
                "Development": 1,
                "Testing": 0,
            }
        },
        {
            "name": "Compete",
            "department": "AI",
            "budget": 1000,
            "tasks_status": {
                "Requirement Gathering": 1,
                "Development": 0,
                "Testing": 0,
            }
        }
    ]
    return render_template("projects.html", data=projects_data)

@app.route("/add_project")
def add_project():
    return render_template("add_projects.html")

@app.route("/employees")
def employees():
    return render_template("employees.html")

@app.route("/logout")
def logout():
    #resp = make_response(render_template("nav_k.html"))
    #resp.delete_cookie("email")
    #resp.delete_cookie("islogin")
    #return resp
    # del session["email"]             
    # del session["islogin"]
    return redirect (url_for("login"))
    #return render_template("nav_k.html")

#@app.route("/emailvalidate/")
#def get_user(var):
    #try:

app.run(host="localhost", port=8080, debug=True)
 