#!/bin/bash

cd push_index && ./main.py 0.01 200 | ./../test_client/main.py test
