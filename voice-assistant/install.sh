#!/bin/bash

sudo apt install portaudio19-dev flac jq libsdl2-dev
python3 -m venv va
source va/bin/activate
pip install -r requirement.txt

