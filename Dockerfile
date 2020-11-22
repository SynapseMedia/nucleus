FROM python:3
LABEL maintainer ="watchit"

ENV PROJECT_ROOT /data/watchit/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT

ADD requeriments.txt .
RUN pip install python-opensubtitles
RUN pip install -r requeriments.txt
COPY . $PROJECT_ROOT