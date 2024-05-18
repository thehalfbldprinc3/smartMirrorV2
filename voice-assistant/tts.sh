#!/bin/bash
echo $* | piper --model /home/ubie/smartMirrorV2/voice-assistant/en_US-lessac-low.onnx --output-raw | \
  aplay -r 22050 -f S16_LE -t raw -

