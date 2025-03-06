#!/usr/bin/bash

python3 ~/src/static-site-generator/src/main.py
cd public && python3 -m http.server 8888