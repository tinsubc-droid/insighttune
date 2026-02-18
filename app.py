from flask import Flask, render_template
import os

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")


# Temporary debug route (you can remove later)
@app.route("/check")
def check():
    return {
        "current_directory": os.getcwd(),
        "files": os.listdir(),
        "templates_exists": os.path.exists("templates"),
        "templates_files": os.listdir("templates") if os.path.exists("templates") else "No templates folder"
    }   
