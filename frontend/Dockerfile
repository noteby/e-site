FROM nginx:1.23.3

ARG FRONTEND_DIR

WORKDIR ${FRONTEND_DIR}

COPY dist dist

CMD [ "nginx", "-g", "daemon off;" ]


