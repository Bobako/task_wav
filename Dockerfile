# syntax=docker/dockerfile:1

FROM  python:3.10

WORKDIR /app_image

COPY config.ini config.ini
COPY main.py main.py
COPY requirments.txt requirments.txt

COPY app app

RUN pip3 install -r requirments.txt
RUN apt-get -y update
RUN apt-get install -y ffmpeg

VOLUME [ "/documents" ]

CMD ["python3", "main.py"]