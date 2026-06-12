#!/bin/bash

set -e

echo "════════════════════════════════════════════════════════════════"
echo "  Ticket Routing Challenge - Environment Setup"
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Installing..."
    sudo apt-get update -qq
    sudo apt-get install -y python3
else
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Found $PYTHON_VERSION"
fi

echo ""
echo "✓ Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found. Installing..."
    sudo apt-get install -y python3-pip
else
    PIP_VERSION=$(pip3 --version)
    echo "✓ Found $PIP_VERSION"
fi

echo ""
echo "✓ Installing Python dependencies..."
pip3 install -q -r requirements.txt

echo ""
echo "✓ Verifying installation..."
python3 -c "import pandas, numpy; print('  • All packages installed successfully')"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  ✓ Setup complete! You can now run:"
echo "    • python3 -m pytest              (run all tests)"
echo "    • python3 app.py                 (run demo)"
echo "════════════════════════════════════════════════════════════════"

