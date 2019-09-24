FROM ubuntu:18.04

ENV LANG="en_US.UTF-8"
RUN apt-get update && apt-get install -y locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    /usr/sbin/update-locale LANG=en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN \
  apt-get update && \
  apt-get install -y python3 python3-pip python3-dev
ADD . /code
WORKDIR /code

RUN pip3 install -r requirements.txt

CMD rq worker sender-tasks --url redis://redis:6379/3 --exception-handler="RQExceptionHandler.writer"