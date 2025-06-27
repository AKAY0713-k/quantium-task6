#!/bin/bash

# Try to activate venv if it exists
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo " Warning: virtual environment not found, continuing without activation."
fi

# Run pytest
pytest

# Check exit code
if [ $? -eq 0 ]; then
    echo " All tests passed."
    exit 0
else
    echo "❌ Some tests failed."
    exit 1
fi
