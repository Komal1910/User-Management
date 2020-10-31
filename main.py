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
    return render_template("profile.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

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
 