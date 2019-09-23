FROM python:3.7.4-alpine
ADD . /code
WORKDIR /code

RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["python3", "server.py"]
