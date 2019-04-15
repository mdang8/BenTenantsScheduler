FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /flask_app
WORKDIR /flask_app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
