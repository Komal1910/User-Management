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
    return redirect (url_for("dashboard"))
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email:
            if password:
                # to be removed -- temporary code
                return redirect (url_for("dashboard"))
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
        # to be removed -- temporary code
        return redirect (url_for("login"))
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        mobile = request.form.get("mobile")
        email = request.form.get("email")
        password = request.form.get("password")
        gender = request.form.get("gender")
        username = email.split("@")[0]
        if email and password:
             try:
                db = sql.connect(host="localhost", port=3306, user="root", password="", database="komal")
             except Exception as e:
                print(e)
                return render_template("signup.html")
             else:
                    cursor = db.cursor()
                    cmd = "select * from user where email='{email}'"
                    cursor.execute(cmd)
                    data = cursor.fetchone()
                    if data:
                        error = "Email already registered"
                        return render_template("Signup.html",error=error)
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
                                msg = MIMEMultipart()
                                from_email = "komal155@gmail.com"
                                msg['To'] = email
                                msg['From'] = "komal1505@gmail.com"
                                msg['Subject'] = "OTP for you account validation"
                                #password = getpass("\n Enter your password : ")
                                passwd= os.environ.get("EMAIL_HOST_PASSWORD")
                                otp = randint(1000,9999)
                                html = """
                                    <html>
                                    <body>
                                    <h1 style='color:#123456;font-style:italic'>This is OTP {otp} for your account validation</h1>
                                    <a href='/localhost/email_validate' style='color:coral;'>Click on this link for email validation</a>                                
                                    </body>
                                    </html>
                                    """
                                    

                                plain = "This is plain message using mime from python script"

                                #msg.attach(m)  #attached the message m
                                
                                #context = ssl.create_default_context()
                                #try:
                                #     with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
                                #         server.login(email,password)
                                #         server.sendmail(email,email,msg.as_string())
                                # except Exception as e:
                                #     return("Error : ",e)
                                # else:
                                #     return render_template("signup.html", error = "Message sent successfully")
                                    #cmd = f"insert into user values ('{fname}','{lname}','{mobile}','{email}','{password}','{gender}','{username}')"
                                    #cursor.execute(cmd)
                                    #db.commit()
                                redirect (url_for("login"))
                            else:
                                error = "Incorrect Password"
                                return render_template("signup.html",error=error)
                        else:
                            error = "Incorrect Password"
                            return render_template("signup.html",error=error)            
        else:
            error = "Invalid Email or password"
            return render_template("Signup.html",error=error)
    else:
        render_template("Signup.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    # get this data from the database and pass to template in the below format
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

@app.route("/add_project_submit", methods=["POST","GET"])
def add_project_submit():
    # insert the data into the db -- projects and project_task_mapping
    if request.method == "GET":
        return render_template("add_projects.html")
    elif request.method == "POST":
        return redirect (url_for("projects"))

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
 