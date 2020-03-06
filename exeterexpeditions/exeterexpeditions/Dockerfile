FROM python:3

LABEL maintainer="University of Exeter Software Development Team O 2020"

RUN apt-get update

RUN mkdir /app

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD [ "mainApp.py" ]