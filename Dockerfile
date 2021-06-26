FROM nikolaik/python-nodejs
LABEL maintainer ="watchit"
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

ENV PROJECT_ROOT /data/watchit/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

# Get dependencies
RUN npm install && npm cache clean --force
RUN pip3 install ipfshttpclient
RUN pip3 install click
RUN pip3 install validators
RUN pip3 install python-dotenv
RUN pip3 install ffmpeg-python
RUN pip3 install coloredlogs
RUN pip3 install verboselogs
RUN pip3 install tqdm
RUN pip3 install gevent
RUN pip3 install -r requirements.txt

