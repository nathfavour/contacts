import re
import sys
from unidecode import unidecode

def remove_emojis(text):
    emoji_pattern = re.compile(
        r'[\U0001F600-\U0001F64F'
        r'\U0001F300-\U0001F5FF'
        r'\U0001F680-\U0001F6FF'
        r'\U0001F700-\U0001F77F'
        r'\U0001F780-\U0001F7FF'
        r'\U0001F800-\U0001F8FF'
        r'\U0001F900-\U0001F9FF'
        r'\U0001FA00-\U0001FA6F'
        r'\U0001FA70-\U0001FAFF'
        r'\U00002600-\U000026FF'
        r'\U00002700-\U000027BF'
        r'\U0000FE00-\U0000FE0F'
        r'\U0001F1E6-\U0001F1FF]+',
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <contacts_csv_path>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    # Normalize stylish/fancy unicode to ASCII
    data = unidecode(data)
    cleaned = remove_emojis(data)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(cleaned)

if __name__ == '__main__':
    main()