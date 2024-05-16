#!/bin/bash

sudo apt install portaudio19-dev flac jq
python3 -m venv va
source va/bin/activate
pip install -r requirement.txt

