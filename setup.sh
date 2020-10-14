#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

printf "\n${RED}Toxic${NC} ${GREEN}Bot${NC}\n\n"

echo "${BLUE}Downloading required files${NC}\n"

cd ToxicBot/

# Install the saved files for GloVe embedding

mkdir -p dump
cd dump/
wget -q --show-progress --progress=bar:force https://github.com/ToxicBot-Discord/ToxicBot/releases/download/v0.0.2/ToxicBot_GloVeEmbedding.json 2>&1
wget -q --show-progress --progress=bar:force https://github.com/ToxicBot-Discord/ToxicBot/releases/download/v0.0.2/ToxicBot_Tokenizer.pickle 2>&1
wget -q --show-progress --progress=bar:force https://github.com/ToxicBot-Discord/ToxicBot/releases/download/v0.0.2/ToxicBot_Weights.h5 2>&1
cd ..
# Create a virtual environment and install python dependencies

echo "${BLUE}Installing a virtual environment and python dependencies${NC}\n"

python3 -m venv env
source env/bin/activate
pip install -r requirements-dev.txt
pre-commit install

# Create the secrets.ini file

echo "${BLUE}Creating the secrets.ini file${NC}\n"

echo "${RED}Enter Discord Bot Token${NC}"
read BOT_TOKEN

echo "Please provide the database configurations\n"
echo "${RED}Database host${NC}"
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

printf "\n${GREEN}Installation Complete${NC}\n\n"
