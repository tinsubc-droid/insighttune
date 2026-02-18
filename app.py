from flask import Flask, request, send_file
from moviepy.editor import *
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "InsightTune Backend Running"

@app.route("/generate", methods=["POST"])
def generate_video():

    mp3 = request.files["mp3"]
    background_img = request.files["background"]
    artist_photo = request.files["photo"]

    title = request.form.get("title", "")
    singer = request.form.get("singer", "")
    cover_by = request.form.get("cover_by", "")

    unique_id = str(uuid.uuid4())

    mp3_path = os.path.join(UPLOAD_FOLDER, unique_id + ".mp3")
    bg_path = os.path.join(UPLOAD_FOLDER, unique_id + "_bg.jpg")
    photo_path = os.path.join(UPLOAD_FOLDER, unique_id + "_photo.jpg")
    output_path = os.path.join(UPLOAD_FOLDER, unique_id + ".mp4")

    mp3.save(mp3_path)
    background_img.save(bg_path)
    artist_photo.save(photo_path)

    audio = AudioFileClip(mp3_path)
    duration = audio.duration

    # Background
    background = ImageClip(bg_path).set_duration(duration).resize((1920,1080))

    # Artist Photo
    photo = ImageClip(photo_path).resize(height=400)
    photo = photo.set_position(("center", 300)).set_duration(duration)

    # Title
    title_text = TextClip(
        title,
        fontsize=80,
        color="white",
        size=(1800,None)
    ).set_position(("center", 750)).set_duration(duration)

    # Info
    info_text = TextClip(
        f"Singer: {singer}   |   Cover By: {cover_by}",
        fontsize=45,
        color="white",
        size=(1800,None)
    ).set_position(("center", 850)).set_duration(duration)

    final = CompositeVideoClip([background, photo, title_text, info_text])
    final = final.set_audio(audio)

    final.write_videofile(output_path, fps=24)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run()
