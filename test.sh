#!/bin/bash

cd push_index && ./main.py 0.5 1 | ./../test_client/main.py test
