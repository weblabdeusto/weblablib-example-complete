# This is the dockerfile to build the lab image that can be used for
# lab development. It does not run a service on its own, the service needs
# to be run explicitly or through docker-compose.

# Inherit from the Alpine image so that the size is particularly small, and using Python 3.6.6.
FROM python:3.6

# This is an alternative to mounting our source code as a volume.
# Originally commented out because docker-compose adds the vol.
ADD . /app

RUN pip install weblablib

WORKDIR /app

ENV FLASK_DEBUG=1
ENV FLASK_APP=autoapp.py
# To serve as a default value (autoapp.py)

RUN pip install -r requirements.txt
