#!/usr/bin/env python3
"""
Fix whitespace issues in Python files.
- Remove trailing whitespace from lines
- Convert lines with only whitespace to empty lines
- Fix blank line spacing issues
"""

import os
import re

def fix_whitespace(file_path):
    """Fix whitespace issues in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        # Remove trailing whitespace
        line = line.rstrip()
        # Convert lines with only whitespace to empty lines
        if re.match(r'^\s+$', line):
            line = ''
        fixed_lines.append(line + '\n')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)

    print(f"Fixed whitespace in: {file_path}")

def main():
    """Main function to process all Python files."""
    # Get all Python files in the project
    python_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                # Skip virtual environment and other non-source directories
                if 'venv' not in root and 'env' not in root and '__pycache__' not in root:
                    python_files.append(os.path.join(root, file))

    # Fix each file
    for file in python_files:
        fix_whitespace(file)

if __name__ == "__main__":
    main()
