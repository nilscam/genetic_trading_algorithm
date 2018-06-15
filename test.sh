#!/bin/bash

cd push_index && ./main.py 0.01 360 | ./../test_client/main.py test
