FROM python:3.7.4-buster
ADD . /code
WORKDIR /code
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN pip3 install --no-cache-dir -r requirements.txt

CMD rq worker sender-tasks --url redis://redis:6379/3 --exception-handler="RQExceptionHandler.writer"
