# https://docs.docker.com/develop/develop-images/multistage-build/
FROM python:3.9
LABEL maintainer ="watchit"
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg

WORKDIR /python
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

FROM node:14

WORKDIR /node
COPY ./package.json .
COPY ./package-lock.json .
COPY --from=0 /python .

RUN npm install --force




