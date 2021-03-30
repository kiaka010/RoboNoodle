FROM python:3.9-alpine

WORKDIR /opt/docroot

#RUN apt-get update
RUN apk add --update musl-dev libffi-dev make gcc git ffmpeg opus-dev

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py