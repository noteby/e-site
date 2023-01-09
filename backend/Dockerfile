FROM python:3.11.1

WORKDIR /e-site/backend

COPY . .

RUN mkdir ~/.pip  && cp pip.conf ~/.pip/

ENTRYPOINT /bin/sh ./start.sh
