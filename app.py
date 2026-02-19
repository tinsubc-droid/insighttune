import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    TextClip,
    ImageClip
)
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ------------------------------
# CONFIGURATION
# ------------------------------
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/downloads"   # changed to match your folder
PROFILE_IMAGE = "static/profile.jpg"
ALLOWED_EXTENSIONS = {"mp3"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ------------------------------
# HELPER FUNCTION
# ------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ------------------------------
# ROUTES
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":
        return "No selected file."

    if not allowed_file(file.filename):
        return "Only MP3 files are allowed."

    title = request.form.get("title", "Untitled Song")
    cover = request.form.get("cover", "Unknown Artist")

    filename = secure_filename(file.filename)
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(input_path)

    # Load audio
    audio = AudioFileClip(input_path)

    # Background
    background = ColorClip(size=(1280, 720), color=(15, 15, 30))
    background = background.set_duration(audio.duration)

    # Title Text
    title_text = TextClip(
        title,
        fontsize=70,
        color="white",
        font="Arial-Bold"
    ).set_position(("center", 200)).set_duration(audio.duration)

    # Cover Text
    cover_text = TextClip(
        f"Covered by {cover}",
        fontsize=40,
        color="lightgray",
        font="Arial"
    ).set_position(("center", 300)).set_duration(audio.duration)

    # Profile Image
    image = ImageClip(PROFILE_IMAGE)
    image = image.resize(height=200)
    image = image.set_position(("center", 420))
    image = image.set_duration(audio.duration)

    # Composite Video
    final_video = CompositeVideoClip(
        [background, title_text, cover_text, image]
    ).set_audio(audio)

    output_filename = filename.rsplit(".", 1)[0] + ".mp4"
    output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_filename)

    final_video.write_videofile(output_path, fps=24)

    # Close clips to free memory
    final_video.close()
    audio.close()

    return send_file(output_path, as_attachment=True)


# ------------------------------
# DEBUG ROUTE (optional)
# ------------------------------
@app.route("/structure")
def structure():
    return {
        "cwd": os.getcwd(),
        "static_exists": os.path.exists("static"),
        "uploads_exists": os.path.exists("static/uploads"),
        "downloads_exists": os.path.exists("static/downloads"),
    }


# ------------------------------
# RUN
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
