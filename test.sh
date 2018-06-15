#!/bin/bash

ENV="server"

if [ "$#" -eq 1 ]; then
    if [ $1 == "local" ]; then
	ENV="local"
    fi
fi

if [ $ENV = "server" ]; then
    cd push_index && ./main.py 0.5 360 | ./../test_client/main.py | ./../server/main.py
else
    cd push_index && ./main.py 0.5 360 | ./../test_client/main.py
fi
