#!/bin/bash
# Minimal installation script for HackerRank environment

# Update package lists
sudo apt-get update -qq 2>&1 | grep -v "NO_PUBKEY" || true

# Install pip3 if not present
if ! command -v pip3 &> /dev/null; then
    sudo apt-get install -y python3-pip 2>&1 | grep -v "^W:"
fi

# Install Python dependencies quietly
pip3 install -q -r requirements.txt

echo "Setup complete. Ready to run tests."

