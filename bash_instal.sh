#!/bin/bash
set -e

sudo apt update
sudo apt install -y libcdd-dev
pip install pycddlib
pip install networkx
