FROM python:3.7

WORKDIR /opt/docroot

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py