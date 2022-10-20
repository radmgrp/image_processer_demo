FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.txt


RUN apt-get update \
    && apt-get install gcc ffmpeg libsm6 libxext6 -y \
    && apt-get clean


COPY . /backend/
