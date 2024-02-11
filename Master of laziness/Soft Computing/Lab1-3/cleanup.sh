#!/bin/bash

# Navigate to the current directory
cd "$(dirname "$0")"

# Find and delete __pycache__ directories in subdirectories
find . -type d -name "__pycache__" -exec rm -r {} +

echo "Cleanup completed."
