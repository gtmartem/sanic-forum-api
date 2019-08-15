FROM python:3.6

RUN mkdir -p /tmp/src

COPY ./ /tmp/src/forum_api

RUN pip install --upgrade pip
RUN pip3 install /tmp/src/forum_api

ENV PYTHONPATH $PYTHONPATH:/tmp/src/forum_api/forum_api
WORKDIR /tmp/src/forum_api/forum_api
