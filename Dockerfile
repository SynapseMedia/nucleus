FROM nikolaik/python-nodejs
LABEL maintainer ="watchit"

ENV PROJECT_ROOT /data/watchit/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

# Get dependencies
RUN npm install && npm cache clean --force
RUN pip3 install ipfshttpclient
RUN pip3 install py-cid
RUN pip3 install validators
RUN pip3 install ffmpeg-python
RUN pip3 install -r requeriments.txt
RUN pip3 install --no-index --find-links resolvers

