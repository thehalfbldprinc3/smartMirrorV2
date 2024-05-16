#!/bin/bash

while true;do

	if [ -e "output.json" ]; then

		text=$(jq -r '.text' output.json)

		echo $text | piper --model en_US-lessac-medium.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw - 

		rm output.json

	fi

	sleep 1

done
