FROM nikolaik/python-nodejs
LABEL maintainer ="watchit"

ENV PROJECT_ROOT /data/watchit/
RUN mkdir -p $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY . $PROJECT_ROOT

# Get dependencies
RUN npm i
RUN pip3 install python-opensubtitles
RUN pip3 install -r requeriments.txt

