#!/usr/bin/env sh

inputHint() {
  echo "#########"
  echo "[$(date "+%Y-%m-%d %H:%M:%S")] $1"
  echo "#########"
}

# Install packages
inputHint "Install packages by pip"

pip install -U pip
pip install -r requirements.txt

# Run
inputHint "Run"

cd ..
uvicorn backend.main:api --host 0.0.0.0 --port 10100 --no-access-log
