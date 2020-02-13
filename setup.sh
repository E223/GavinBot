#!/bin/sh

mkdir -p ./clips/laughs/
mkdir -p ./clips/questions/
mkdir -p ./clips/responses/
mkdir -p ./clips/testing/
mkdir -p ./logs/

if [ "$1" == "no-install" ]; then
    echo "Not installing python packages"
else
    sudo apt install ffmpeg
    python3.8 -m pip install -U python-dotenv
    python3.8 -m pip install -U discord.py[voice]
fi

cp -n .env.example .env

echo "Setup complete."