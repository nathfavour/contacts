import pandas as pd
import re
import sys
from unidecode import unidecode

def is_meaningful_name(name):
    """Check if a name is meaningful (not just numbers, import metadata, etc.)"""
    if not name or len(name.strip()) == 0:
        return False
    
    name = name.strip()
    
    # Skip import metadata and common non-name patterns
    skip_patterns = [
        r'^imported\s+on',
        r'^\d+$',  # Only numbers
        r'^_+$',   # Only underscores
        r'^\d+_*$', # Numbers with trailing underscores
        r'^_*\d+_*$', # Numbers with underscores
    ]
    
    for pattern in skip_patterns:
        if re.match(pattern, name, re.IGNORECASE):
            return False
    
    # Consider meaningful if it starts with a letter or contains letters
    return bool(re.search(r'[a-zA-Z]', name))

def find_best_name(row):
    """Find the most meaningful name from all available fields"""
    # Define name fields in order of preference
    name_fields = [
        'First Name', 'Middle Name', 'Last Name',
        'Nickname', 'File As', 
        'Phonetic First Name', 'Phonetic Middle Name', 'Phonetic Last Name',
        'Name Prefix', 'Name Suffix',
        'Organization Name', 'Organization Title'
    ]
    
    # Collect all potential names
    candidates = []
    for field in name_fields:
        value = row.get(field, '')
        if value and str(value).strip():
            candidates.append(str(value).strip())
    
    # Find the first meaningful name
    for candidate in candidates:
        if is_meaningful_name(candidate):
            return candidate
    
    # If no meaningful name found, return the first non-empty value
    for candidate in candidates:
        if candidate:
            return candidate
    
    return ''

def canonize_name(row):
    # First try to find the best meaningful name
    best_name = find_best_name(row)
    
    if best_name:
        name = best_name
    else:
        # Fallback to concatenating all name fields
        name_fields = [
            row.get('First Name', ''),
            row.get('Middle Name', ''),
            row.get('Last Name', ''),
            row.get('Phonetic First Name', ''),
            row.get('Phonetic Middle Name', ''),
            row.get('Phonetic Last Name', ''),
            row.get('Name Prefix', ''),
            row.get('Name Suffix', ''),
            row.get('Nickname', ''),
            row.get('File As', ''),
        ]
        name = ' '.join([str(n) for n in name_fields if str(n).strip()])
    
    # Normalize stylish/fancy unicode to ASCII
    name = unidecode(name)
    # Replace any remaining non a-z, non-digit, non-space with underscore
    name = re.sub(r'[^a-zA-Z0-9 ]', '_', name)
    # Convert spaces to underscores
    name = re.sub(r'\s+', '_', name)
    # Replace any character repeated 3 or more times with a single instance
    name = re.sub(r'(.)\1{2,}', r'\1', name)
    # Remove leading underscores
    name = re.sub(r'^_+', '', name)
    # If name is a single character, append underscore
    if len(name) == 1:
        name = name + '_'
    
    return name

def main():
    if len(sys.argv) < 2:
        print("Usage: python process.py <contacts_csv_path>")
        sys.exit(1)
    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path, dtype=str)
    df.fillna('', inplace=True)
    # Apply canonization
    df['First Name'] = df.apply(canonize_name, axis=1)
    # Ensure unique names
    name_count = {}
    new_names = []
    for name in df['First Name']:
        base = name
        if base not in name_count:
            name_count[base] = 0
            new_names.append(base)
        else:
            name_count[base] += 1
            new_names.append(f"{base}_{name_count[base]}")
    df['First Name'] = new_names
    # Clear other name columns
    for col in ['Middle Name', 'Last Name', 'Phonetic First Name', 'Phonetic Middle Name', 'Phonetic Last Name', 'Name Prefix', 'Name Suffix', 'Nickname', 'File As']:
        if col in df.columns:
            df[col] = ''
    # Write back, preserve structure
    df.to_csv(csv_path, index=False)

if __name__ == '__main__':
    main()
