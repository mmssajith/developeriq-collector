FROM python:3.11.6-slim

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

RUN pip install -r requirements.txt --src /usr/src/app

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
EXPOSE 80
CMD ["./start.sh"]
