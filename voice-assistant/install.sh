#!/bin/bash

sudo apt install portaudio19-dev flac jq libsdl2-dev build-essential swig  libpulse-dev libasound2-dev ffmpeg
python3 -m venv va
source va/bin/activate
pip install -r requirement.txt

