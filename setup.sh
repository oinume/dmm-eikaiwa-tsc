#!/bin/sh

if [ ! -d venv ]; then
    virtualenv --python=/usr/local/bin/python3.5 --distribute venv
    . venv/bin/activate
    pip install -r requirements/development.txt
fi
