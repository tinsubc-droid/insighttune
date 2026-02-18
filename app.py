import os
import traceback
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

# If you later re-enable video generation
from moviepy.editor import ImageClip, AudioFileClip

app = Flask(__name__)

# Folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ---------------------------
# HOME ROUTE
# ---------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------
# GENERATE ROUTE
# ---------------------------
@app.route("/generate", methods=["POST"])
def generate_video():
    try:
        # Check files
        if "audio" not in request.files or "image" not in request.files:
            return "Audio or Image not uploaded", 400

        audio_file = request.files["audio"]
        image_file = request.files["image"]

        if audio_file.filename == "" or image_file.filename == "":
            return "No file selected", 400

        # Save uploaded files
        audio_filename = secure_filename(audio_file.filename)
        image_filename = secure_filename(image_file.filename)

        audio_path = os.path.join(UPLOAD_FOLDER, audio_filename)
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)

        audio_file.save(audio_path)
        image_file.save(image_path)

        # 🔥 TEMPORARY SAFE TEST MODE
        # Return success first to confirm backend works
        return "Files uploaded successfully ✅"

        # ----------------------------------------
        # AFTER CONFIRMING WORKS, UNCOMMENT BELOW
        # ----------------------------------------

        """
        audio = AudioFileClip(audio_path)
        image = ImageClip(image_path)

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
        """

    except Exception:
        return f"<pre>{traceback.format_exc()}</pre>"


# ---------------------------
# RUN (For local testing only)
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
