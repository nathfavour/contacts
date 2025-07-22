import pandas as pd
import re
import sys

def canonize_name(row):
    # Concatenate all name fields
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
    # Join non-empty fields with space
    name = ' '.join([str(n) for n in name_fields if str(n).strip()])
    # Remove non a-z and non-digit characters (case-insensitive, keep spaces)
    name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
    # Convert spaces to underscores
    name = re.sub(r'\s+', '_', name)
    # Remove repeating characters (3 or more)
    name = re.sub(r'(.)\1{2,}', r'\1', name)
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
