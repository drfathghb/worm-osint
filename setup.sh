#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt
mkdir -p data reports wordlists logs
echo "Done! Run: python main.py"
