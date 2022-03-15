FROM python:3.7-bullseye

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y ffmpeg tesseract-ocr tesseract-ocr-lav

COPY . /app
WORKDIR /app

# Expose the Flask port
EXPOSE 5000

CMD [ "python", "-u", "./main.py" ]
