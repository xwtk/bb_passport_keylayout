# Keyboard Layouts for BlackBerry Passport running Android software
Keyboard layouts adapted for use with the BlackBerry Passport 3-row keyboard.

# How to contribute
* Commit changes to the generate_kcm.py, check CHARACTER_MAPPINGS to find your language, if your language isn't there, add it, update LANGUAGE_NAMES.
* Commit changes to languages.csv

For example:
```
    'hy': {  # Armenian
        'Q': ('ք', 'Ք'), 'W': ('ո', 'Ո'), 'E': ('ե', 'Ե'), 'R': ('ռ', 'Ռ'), 'T': ('տ', 'Տ'),
        'Y': ('ը', 'Ը'), 'U': ('ւ', 'Ւ'), 'I': ('ի', 'Ի'), 'O': ('օ', 'Օ'), 'P': ('պ', 'Պ'),
        'A': ('ա', 'Ա'), 'S': ('ս', 'Ս'), 'D': ('դ', 'Դ'), 'F': ('ֆ', 'Ֆ'), 'G': ('գ', 'Գ'),
        'H': ('հ', 'Հ'), 'J': ('յ', 'Յ'), 'K': ('կ', 'Կ'), 'L': ('լ', 'Լ'),
        'Z': ('զ', 'Զ'), 'X': ('ղ', 'Ղ'), 'C': ('ց', 'Ց'), 'V': ('վ', 'Վ'), 'B': ('բ', 'Բ'),
        'N': ('ն', 'Ն'), 'M': ('մ', 'Մ')
    },
```
You need to map the appropriate letter of your alphabet to the latin letter on the keyboard.

# Contributing to languages.csv
You may also add your language to languages.csv if not found previously, ensure that you match the format, if you find it useful to compile multiple layouts, add the appropriate filename. You may leave a row blank if not needed (for example if you only need AZERTY).
