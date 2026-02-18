from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Server is Working ✅</h1>
    """
