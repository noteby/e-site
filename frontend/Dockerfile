FROM nginx:1.23.3

WORKDIR /var/www/e-site/frontend

COPY dist dist

#COPY start.sh .
#ENTRYPOINT /bin/sh ./start.sh

CMD [ "nginx", "-g", "daemon off;" ]


