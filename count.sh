#!/bin/bash
topic=$1
_topic="./logs/${topic}"
file=$(ls "${_topic}")
path="${_topic}/${file}"
number=$(tail -n 1 ${path} | cut -d : -f 3)
echo the number of consumed messages from the topic ${topic} is ${number}
