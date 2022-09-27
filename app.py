from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, session
from model import create_post, fetch_posts, authenticate_user, register_user
from flask_session import Session
# from flask_cors import CORS

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def homepage():
	return render_template("login.html")

@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		username = request.form.get("username", None)
		password = request.form.get("password", None)
		if username and password:
			if authenticate_user(username, password):
				session["username"] = username
				return render_template("redirectLogin.html", username=session["username"])
			else:
				return render_template("login.html", msg="error")

@app.route("/registerPage", methods=["POST", "GET"])
def registerPage():
	return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
	if request.method == "POST":
		username = request.form.get("username", None)
		password = request.form.get("password", None)
		if username and password:
			register_user(username, password)
			return render_template("login.html")

@app.route("/post", methods=["GET", "POST"])
def postpage():
	if request.method == "POST":
		username = request.form.get("username", None)
		content = request.form.get("content", None)
		dt = datetime.now()
		if username and content:
			create_post(username, content, dt)

	posts = fetch_posts()
	return render_template("index.html", posts=posts, username=session["username"])

if __name__ == "__main__":
	app.run(debug=True)