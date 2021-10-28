FROM nikolaik/python-nodejs:python3.9-nodejs17
LABEL maintainer ="watchit"
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

ENV PROJECT_ROOT /data/watchit/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

# Install deps
RUN npm install && npm cache clean --force
RUN pip3 install -r requirements.txt

