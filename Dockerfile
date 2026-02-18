FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (important)
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Use Render provided PORT
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]
