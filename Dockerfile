# https://docs.docker.com/develop/develop-images/multistage-build/
FROM python:3.10 as python
LABEL maintainer ="watchit"
RUN apt update 
RUN apt-get install -y --no-install-recommends ffmpeg
RUN apt-get install libsqlite3-dev

WORKDIR /usr/share/python
# Add requirements to build context
COPY requirements.txt . 

# Educative commentary :).
# Why we use pyhon3 and not just python?
# Is possible that if we use just `python` an `alternative` could be set as python 2.x
# Is hard to say when an `alternative` is set for python 3 so we enforce it.
# Using `python3` enforce usage of 3.x version of python
# Check this discussion: https://stackoverflow.com/questions/64801225/python-or-python3-what-is-the-difference

# Upgrade pip before install
RUN python3 -m pip install --upgrade pip 
# Install dependencies
RUN python3 -m pip install -r requirements.txt


# Remove cache, byte-code cache, test files or directories
# This reduces the size of the python libs by about 50%
ENV PY_PATH=/usr/local/lib/python3.10/
RUN find ${PY_PATH} -type d -a -name test -exec rm -rf '{}' +
RUN find ${PY_PATH} -type d -a -name tests  -exec rm -rf '{}' +
RUN find ${PY_PATH} -type f -a -name '*.pyc' -exec rm -rf '{}' +
RUN find ${PY_PATH} -type f -a -name '*.pyo' -exec rm -rf '{}' +

FROM node:14 as stage
# Set default entry directory
ENV WORK_DIR = /data/watchit
# Create workdir before using
RUN mkdir -p ${WORK_DIR}
WORKDIR /${WORK_DIR}


COPY ./package.json .
COPY ./package-lock.json .
COPY --from=python /usr/local/lib/python3.10/ /usr/local/lib/python3.10/

# Install dependencies
RUN npm install --force




