#!/bin/sh

if [ ! -d venv ]; then
    virtualenv --distribute venv
    . venv/bin/activate
    pip install -r requirements.txt
fi
