import os
import traceback
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    try:
        return "App is running correctly ✅"
    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"
