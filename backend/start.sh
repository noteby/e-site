#!/usr/bin/env sh

stepInfo() {
  echo "##################################"
  echo "#"
  echo "# $(date "+%Y-%m-%d %H:%M:%S") $1"
  echo "#"
  echo "##################################"
}

## Install Sqlite3
# https://www.sqlite.org/download.html
# https://www.sqlite.org/2022/sqlite-autoconf-3400100.tar.gz
command -v sqlite3 >/dev/null 2>&1 || {
  stepInfo "Install Sqlite3"

  sqlite3_pkg="sqlite-autoconf-3400100"

  ls ./store/${sqlite3_pkg}.tar.gz >/dev/null 2>&1 || {
    echo "#) Download sqlite3 pkg..."
    wget https://www.sqlite.org/2022/${sqlite3_pkg}.tar.gz -P ./store/
  }

  echo "#) Uncompress sqlite3 pkg..."
  tar -zxvf ./store/${sqlite3_pkg}.tar.gz -C /opt/

  echo "#) Compile sqlite3 code..."
  cd /opt/${sqlite3_pkg} || exit
  ./configure && make && make install

  echo "#) Delete sqlite3 pkg..."
  cd - >/dev/null || exit
  rm -rf /opt/${sqlite3_pkg}
}

## Startup api
stepInfo "Startup api"

cd ..
uvicorn backend.main:api --host 0.0.0.0 --port 10100 --no-access-log
