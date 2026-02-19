FROM python:3.11-slim

# Install ImageMagick
RUN apt-get update && \
    apt-get install -y imagemagick && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
