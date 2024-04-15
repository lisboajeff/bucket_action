#!/bin/bash

CONFIG_PATH="$1"
FILE_DIRECTORY="$2"
EXTENSION="$3"

VENV="/tmp/venv_bucket"
SOURCE="src"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Install Python 3 to continue."
    exit 1
fi

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <FILE_DIRECTORY> <EXTENSION>"
    exit 1
fi

if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
    echo "Virtual environment '$VENV' created."
else
    echo "The virtual environment '$VENV' already exists."
fi

source "$VENV/bin/activate"

if [ ! -f "requirements.txt" ]; then
    echo "File requirements.txt not found."
    exit 1
else
    pip install -r "requirements.txt"
fi

if [ ! -f "$CONFIG_PATH" ]; then
    echo "Configuration file not found: $CONFIG_PATH"
    exit 1
fi

set -a
# shellcheck disable=SC1090
source "$CONFIG_PATH"
set +a

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
echo "AWS Access Key ID and/or AWS Secret Access Key have not been set as environment variables."   exit 1
fi

python3 "$SOURCE/main.py" "$FILE_DIRECTORY:$EXTENSION"

rm s3_sync_report.md