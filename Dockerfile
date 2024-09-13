FROM python:3.10.12

WORKDIR /backend_api

ADD . .

RUN apt-get update && apt-get install -y python3-openssl

RUN pip install -r requirements.txt


ENV POSTGRES_HOST=None
ENV POSTGRES_PORT=None
ENV POSTGRES_DB=None
ENV POSTGRES_USER=value
ENV POSTGRES_PASSWORD=value
ENV APP_PORT=9090


EXPOSE 80

CMD [ "python3", "app/main.py" ]