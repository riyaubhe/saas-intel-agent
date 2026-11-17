#!/bin/bash
# sets everything up. run with: bash setup.sh

set -e

echo "making venv..."
python3 -m venv venv
source venv/bin/activate

echo "installing packages..."
pip install -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "made a .env file, put your gemini api key in it"
fi

echo "running tests..."
pytest

echo "done!"
