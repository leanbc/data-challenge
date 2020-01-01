#!/bin/bash
topic=$1
topic="./logs/${topic}"
file=$(ls "${topic}")
path="${topic}/${file}"
tail -n 1 $path | cut -d : -f 3
