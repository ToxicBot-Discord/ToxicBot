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
wget -q --show-progress --progress=bar:force https://github.com/Sid200026/ToxicBot/releases/download/v0.0.2/ToxicBot_GloVeEmbedding.json 2>&1
wget -q --show-progress --progress=bar:force https://github.com/Sid200026/ToxicBot/releases/download/v0.0.2/ToxicBot_Tokenizer.pickle 2>&1
wget -q --show-progress --progress=bar:force https://github.com/Sid200026/ToxicBot/releases/download/v0.0.2/ToxicBot_Weights.h5 2>&1
cd ..
# Create a virtual environment and install python dependencies

echo "${BLUE}Installing a virtual environment and python dependencies${NC}\n"

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Create the secrets.ini file

echo "${BLUE}Creating the secrets.ini file${NC}\n"

echo "${RED}Enter Discord Bot Token${NC}"
read BOT_TOKEN

touch secret.ini
echo "[Discord]\n
BOT_TOKEN=${BOT_TOKEN}\n
" >secret.ini

printf "\n${GREEN}Installation Complete${NC}\n\n"
