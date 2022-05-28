# https://docs.docker.com/develop/develop-images/multistage-build/
FROM python:3.10
LABEL maintainer ="watchit"
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg
RUN apt-get install python3.10-venv -y
RUN apt-get install python3.10-distuils -y
WORKDIR /python
COPY requirements.txt /python

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM node:14-alpine
ENV PROJECT_ROOT /data/watchit/
WORKDIR $PROJECT_ROOT

COPY package.json $PROJECT_ROOT
COPY package-lock.json $PROJECT_ROOT

# Install deps
RUN npm install --force
COPY --from=0 /python ./




