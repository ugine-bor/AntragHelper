import os
from deep_translator import GoogleTranslator
from polib import pofile
from pathlib import Path


# Function to translate text using Deepl Google Translator
def translate_text(text, target_lang):
    translator = GoogleTranslator(source='auto', target=target_lang)
    translated_text = translator.translate(text)
    return translated_text


# Function to translate .po file to the specified language.txt and save the result
def translate_po_file(po_file_path, target_lang):
    po = pofile(po_file_path)
    untranslated_entries = [entry for entry in po if not entry.msgstr]

    if not untranslated_entries:
        print(f"No untranslated strings in {po_file_path} for {target_lang}. Skipping...")
        return

    for entry in untranslated_entries:
        # Perform the translation
        translated_text = translate_text(entry.msgid, target_lang)

        # Update the msgstr with the translation
        entry.msgstr = translated_text

    # Save the translated .po file
    po.save(po_file_path)

    print(f'{po_file_path} -> {po_file_path} (Translated to {target_lang})')


# Directory containing the .po files
po_files_directory = 'locales'

# List of target languages for translation
target_languages = ['de', 'en', 'fa', 'ru']

# Translate .po files for each target language.txt
for root, _, files in os.walk(po_files_directory):
    for file in files:
        print(f'{file}')
        if file.endswith('.po'):
            po_file_path = os.path.join(root, file)
            print(str(Path(po_file_path).parent.parent)[-2:])
            translate_po_file(po_file_path, str(Path(po_file_path).parent.parent)[-2:])

# NAME CAN BE INVALID. START WORKS
# pybabel extract -o locales/start.pot -k __ -k _n:1,2 -k _p:1,2 -k _np:1,2,4 .   1
# pybabel init -i locales/start.pot -d locales -D start -l en
# run POtranslator(translate all .po)   3
# pybabel compile -d locales -D start   4
# pybabel update -d locales -D start -i locales/start.pot   2

# for single script
# pybabel extract -o locales/start.pot -k __ -k _n:1,2 -k _p:1,2 -k _np:1,2,4 handlers/users/start.py   1
# pybabel init -i locales/start.pot -d locales -D start -l en
# run POtranslator(translate all .po)   3
# pybabel compile -d locales -D start   4
# pybabel update -d locales -D start -i locales/start.pot   2
