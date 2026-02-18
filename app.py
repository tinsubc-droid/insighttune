import os
import traceback
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_video():
    try:
        if "audio" not in request.files or "image" not in request.files:
            return "Audio or Image not uploaded", 400

        audio_file = request.files["audio"]
        image_file = request.files["image"]

        if audio_file.filename == "" or image_file.filename == "":
            return "No file selected", 400

        audio_filename = secure_filename(audio_file.filename)
        image_filename = secure_filename(image_file.filename)

        audio_file.save(os.path.join(UPLOAD_FOLDER, audio_filename))
        image_file.save(os.path.join(UPLOAD_FOLDER, image_filename))

        return "Files uploaded successfully ✅"

    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
