FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /BookAnAppointment

ADD . /BookAnAppointment

COPY ./requirements.txt /BookAnAppointment/requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt



