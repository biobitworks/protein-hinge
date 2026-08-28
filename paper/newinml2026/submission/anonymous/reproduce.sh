#!/bin/sh
set -e
python3 methods/normalize.py
python3 -c "import json; json.load(open('methods/alias_table.json'))"
