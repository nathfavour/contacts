# Contacts CSV Cleaner

This project provides Python scripts to clean and restructure your contacts CSV file.  
It removes emojis, canonizes contact names, and ensures consistent formatting.

## Features

- **Remove emojis** from all fields.
- **Canonize contact names**: merges all name fields into a single first name, removes non a-z characters, converts spaces to underscores, and removes repeating characters (3+).
- **Preserves CSV structure**.

## Requirements

- Python 3.7+
- pandas

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Remove Emojis

```bash
python script.py <contacts_csv_path>
```

### Canonize and Clean Contact Names

```bash
python process.py <contacts_csv_path>
```

## Files

- `script.py`: Removes emojis from the CSV.
- `process.py`: Canonizes and cleans contact names.
- `requirements.txt`: Python dependencies.

## Notes

- Always back up your original CSV before running these scripts.
- The scripts overwrite the input CSV file.
