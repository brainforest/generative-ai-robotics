#!/bin/bash

# Directory to search, default is the current directory
DIR=${1:-.}

# Output file to save the imports
OUTPUT_FILE="python_imports.txt"

# Temporary file to collect all imports
TEMP_FILE=$(mktemp)

# Clear the output file if it exists
> $OUTPUT_FILE

# Find all Python files and extract lines with 'import'
find "$DIR" -name "*.py" -type f | while read -r file
do
    #echo "Processing $file..." >> $OUTPUT_FILE
    grep -E "^import |^from " "$file" >> $TEMP_FILE
done

# Sort and make the imports unique, then save them to the output file
sort $TEMP_FILE | uniq >> $OUTPUT_FILE

# Clean up the temporary file
rm $TEMP_FILE

echo "Unique, sorted imports have been saved to $OUTPUT_FILE"

