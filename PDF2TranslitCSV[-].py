import PyPDF2
from deep_translator import GoogleTranslator
import os


def translate_first_word_in_lines(input_file, output_file, target_language='ru'):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            words = line.split(';')
            if words:
                first_word = words[0].strip()
                if first_word:
                    translated_word = GoogleTranslator(source='de', target=target_language).translate(first_word)
                    translated_line = line.replace(first_word, translated_word, 1)  # Replace only the first occurrence
                    outfile.write(translated_line)


def extract_text_from_textboxes(pdf_path):
    boxes_info = {}
    counter = 0

    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            annotations = page['/Annots']
            if annotations:
                for annotation in annotations:
                    if counter > 2:
                        return boxes_info
                    annot_object = annotation.get_object()
                    if annot_object.get('/Subtype') == '/Widget':
                        box_name = annot_object.get('/TU')
                        if annot_object.get('/FT') == '/Tx':
                            boxes_info[box_name] = "text"
                            counter += 1
                        elif annot_object.get('/FT') == '/Btn':
                            boxes_info[box_name] = "check"
                            counter += 1

    return boxes_info


def csvtotranslit(pathin, pathout, separ=','):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '',
        'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', ' ': ' ', '(': '(', ')': ')', ',': ',', ':': ':', '1': '1', '2': '2', '3': '3',
        '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9', '0': '0', '-': '-', '.': '.', '«': '«', '»': '»'
    }
    result = ''
    with open(pathin, "rt", encoding="utf-8") as fin, open(pathout, "wt", encoding="utf-8") as fout:
        lines = fin.readlines()
        for line in lines:
            k, v = line.split(';')
            fout.write(f"{''.join([translit_dict[i] for i in k])}{separ}{v}")
    return result


if __name__ == "__main__":
    mydict = {'Kundennummer falls bekannt': '1234576789', 'Vorname': 'John', 'Gebutsdatum': '23.10.1990',
              'Familienname': 'Doe', 'Geburtsdatum': '23.10.1990', 'Nachname': 'Doe', 'Geschlecht': 'Herr',
              'Geburtsname (sofern abweichend)': '-'}

    filestoparse = os.listdir(r"C:\Users\ugine\Downloads\formulars")
    for f in filestoparse:
        pdf_file_path = fr"C:\Users\ugine\Downloads\formulars\{f}"
        textboxes = extract_text_from_textboxes(pdf_file_path)
        textboxes = textboxes.items()
        with open(r"C:\Users\ugine\Downloads\Sampl.csv", "wt", encoding="utf-8") as fout:
            for k, v in textboxes:
                fout.write(f"{k};{mydict.get(k,v)}\n")
        translate_first_word_in_lines(r"C:\Users\ugine\Downloads\Sampl.csv", r"C:\Users\ugine\Downloads\rusSampl.csv",
                                      "ru")
        csvtotranslit(r"C:\Users\ugine\Downloads\rusSampl.csv", fr"C:\Users\ugine\Downloads\Samples\{f[:-4]}.csv", ';')
