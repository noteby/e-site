FROM python:3.11.1

ARG BACKEND_DIR

WORKDIR ${BACKEND_DIR}

COPY . .

RUN mkdir ~/.pip  &&  \
    cp pip.conf ~/.pip/ &&  \
    pip install -U pip &&  \
    pip install -r requirements.txt

ENV LD_LIBRARY_PATH=/usr/local/lib

ENTRYPOINT ["sh", "start.sh"]
