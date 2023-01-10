FROM python:3.11.1

ARG WORK_DIR=/e-site/backend

WORKDIR ${WORK_DIR}

COPY . .

#RUN mkdir ~/.pip  && cp pip.conf ~/.pip/ &&  \
#    cd .. &&  \
#    wget https://www.sqlite.org/2022/sqlite-autoconf-3400100.tar.gz && \
#    tar -zxvf sqlite-autoconf-3400100.tar.gz &&  \
#    cd sqlite-autoconf-3400100 &&  \
#    ./configure &&  \
#    make && make install && \
#    cd ${WORK_DIR}

COPY store/sqlite-autoconf-3400100.tar.gz ..

RUN mkdir ~/.pip  && cp pip.conf ~/.pip/ &&  \
    pip install -U pip && pip install -r requirements.txt && \
    cd .. && tar -zxvf sqlite-autoconf-3400100.tar.gz &&  \
    cd sqlite-autoconf-3400100 &&  \
    ./configure && make && make install && \
    cd .. && rm -rf sqlite-autoconf-3400100* && \
    cd ${WORK_DIR}

ENV LD_LIBRARY_PATH=/usr/local/lib

ENTRYPOINT /bin/sh ./start.sh
