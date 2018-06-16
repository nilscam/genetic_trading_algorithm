#!/bin/bash

ENV="server"

if [ "$#" -eq 1 ]; then
    if [ $1 == "local" ]; then
	ENV="local"
    fi
fi

if [ $ENV = "server" ]; then
    cd push_index && ./main.py 0.05 360 | ./../test_client/trade | ./../server/main.py
else
    cd push_index && ./main.py 0.001 360 | ./../test_client/trade
fi
