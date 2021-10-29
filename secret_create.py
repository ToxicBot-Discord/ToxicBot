import os

class colors:
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color

directory = 'secret'

if not os.path.exists(directory):
    os.makedirs(directory)

print(f"{colors.BLUE}Creating the secrets.ini file{colors.NC}")

print(f"{colors.RED}Enter Discord Bot Token{colors.NC}")
BOT_TOKEN = input()

print(f"{colors.RED}Please provide the database configurations\n{colors.NC}")
print(f"{colors.RED}Database host ( Use db if using docker postgres service ){colors.NC}")

HOST = input()

print(f"{colors.RED}Database port{colors.NC}")

PORT = input()

print(f"{colors.RED}Database user{colors.NC}")

USER = input()

print(f"{colors.RED}Database password{colors.NC}")
PASSWORD = input()

print(f"{colors.RED}Database name{colors.NC}")
DATABASE = input()

secret_format = f"\
[DISCORD]\n\
BOT_TOKEN={BOT_TOKEN}\n\
\n\
[DATABASE]\n\
DATABASE={DATABASE}\n\
USER={USER}\n\
PASSWORD={PASSWORD}\n\
HOST={HOST}\n\
PORT={PORT}\n\
"

env_fornat = f"\
PYTHON_VERSION=3.8\n\
POSTGRES_VERSION=13-alpine\n\
WORKDIR=app\n\
SECRET_DIR=secret\n\
SECRET_FILE=secret.ini\n\
IMAGE_NAME=sid200026/toxicbot\n\
IMAGE_TAG=1.0.0\n\
POSTGRES_PASSWORD={PASSWORD}\n\
POSTGRES_USER={USER}\n\
POSTGRES_DB={DATABASE}\n\
POSTGRES_PORT={PORT}\n\
"

with open('secret/secret.ini', "w+") as file:
    file.write(secret_format)

with open('.env', "w+") as file:
    file.write(env_fornat)