#!/bin/bash
# Should be run from the directory it is in
echo "  [+] Deploying Reciving Server"
echo "   |  Installing Dependancies"
sudo apt update && sudo apt install -y python3-venv python3-full
echo "   |  Configuring Venv"
python3 -m venv .venv
source ./.venv/bin/activate
echo "   |  Installing FLASK"
python3 -m pip install flask
echo "  [+]  Starting Server"
python3 app.py

