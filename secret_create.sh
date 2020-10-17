#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create the secrets.ini file

mkdir -p secret
cd secret/

echo "${BLUE}Creating the secrets.ini file${NC}\n"

echo "${RED}Enter Discord Bot Token${NC}"
read BOT_TOKEN

echo "Please provide the database configurations\n"
echo "${RED}Database host ( Use db if using docker postgres service ) ${NC}"
read HOST
echo "${RED}Database port${NC}"
read PORT
echo "${RED}Database user${NC}"
read USER
echo "${RED}Database password${NC}"
read PASSWORD
echo "${RED}Database name${NC}"
read DATABASE

touch secret.ini
echo "[DISCORD]
BOT_TOKEN=${BOT_TOKEN}

[DATABASE]
DATABASE=${DATABASE}
USER=${USER}
PASSWORD=${PASSWORD}
HOST=${HOST}
PORT=${PORT}
" >secret.ini

cd ..

touch .env
echo "PYTHON_VERSION=3.8
POSTGRES_VERSION=13-alpine
WORKDIR=app
SECRET_DIR=secret
SECRET_FILE=secret.ini
IMAGE_NAME=sid200026/toxicbot
IMAGE_TAG=1.0.0
POSTGRES_PASSWORD=${PASSWORD}
POSTGRES_USER=${USER}
POSTGRES_DB=${DATABASE}
POSTGRES_PORT=${PORT}
" >.env
