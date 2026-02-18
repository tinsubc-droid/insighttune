import os
from flask import Flask, render_template, request, send_file
from moviepy.editor import ImageClip, AudioFileClip
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Create folders if not exist
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_video():
    try:
        if "audio" not in request.files or "image" not in request.files:
            return "Audio or Image not uploaded"

        audio_file = request.files["audio"]
        image_file = request.files["image"]

        if audio_file.filename == "" or image_file.filename == "":
            return "No file selected"

        # Secure filenames
        audio_filename = secure_filename(audio_file.filename)
        image_filename = secure_filename(image_file.filename)

        audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)

        audio_file.save(audio_path)
        image_file.save(image_path)

        # Load media
        audio = AudioFileClip(audio_path)
        image = ImageClip(image_path)

        # Set video duration equal to audio
        video = image.set_duration(audio.duration)
        video = video.set_audio(audio)

        output_path = os.path.join(OUTPUT_FOLDER, "final_video.mp4")

        video.write_videofile(
            output_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return f"Error occurred: {str(e)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
