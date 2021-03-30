FROM python:3.9

WORKDIR /opt/docroot

RUN apt-get update
RUN apt-get -y install ffmpeg

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py