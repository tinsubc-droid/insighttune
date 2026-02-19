import os
from flask import Flask, render_template, request, send_file
from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    TextClip,
    ImageClip
)
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
PROFILE_IMAGE = "static/profile.jpg"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files["file"]
    title = request.form["title"]
    cover = request.form["cover"]

    filename = secure_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(input_path)

    audio = AudioFileClip(input_path)

    # Background
    background = ColorClip(size=(1280, 720), color=(15, 15, 30))
    background = background.set_duration(audio.duration)

    # Song Title Text
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
    image = image.set_position(("center", 400))
    image = image.set_duration(audio.duration)

    final_video = CompositeVideoClip(
        [background, title_text, cover_text, image]
    ).set_audio(audio)

    output_filename = filename.rsplit(".", 1)[0] + ".mp4"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    final_video.write_videofile(output_path, fps=24)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
