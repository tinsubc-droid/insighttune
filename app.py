import traceback
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    try:
        return render_template("index.html")
    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"
