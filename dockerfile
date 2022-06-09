FROM python:3
FROM ubuntu

RUN set -xe \
    && apt-get update -y \
    && apt-get install -y python3-pip

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]