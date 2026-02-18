from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/structure")
def structure():
    return {
        "cwd": os.getcwd(),
        "files_here": os.listdir(),
        "templates_exists": os.path.exists("templates"),
        "templates_content": os.listdir("templates") if os.path.exists("templates") else "NO"
    }
