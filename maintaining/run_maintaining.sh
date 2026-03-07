#!/bin/bash
cd "$(dirname "$0")/.."

mkdir -p data

echo "Running maintenance scripts..."
echo

FAILED=0

for script in maintaining/*.py; do
    echo "Running $script..."
    PYTHONPATH="$(pwd)" python "$script"
    if [ $? -ne 0 ]; then
        echo "$script failed."
        FAILED=1
    else
        echo "$script completed."
    fi
    echo
done

if [ $FAILED -eq 1 ]; then
    echo "One or more scripts failed."
    exit 1
else
    echo "All scripts completed successfully."
fi
