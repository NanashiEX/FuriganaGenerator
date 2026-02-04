from sudachipy import dictionary
import pykakasi
from difflib import SequenceMatcher
import re
import json

tokenizer = dictionary.Dictionary().create()
kakasi = pykakasi.kakasi()

# Loading the JLPT dict outside so it'll only load once.
# Assume jlpt_dict is a simple { "word": level_int }
with open('jlpt_lookup.json', 'r', encoding='utf-8') as f:
    JLPT_DICT = json.load(f)
# This regex matches the Unicode range for Japanese Kanji
KANJI_PATTERN = re.compile(r'[㐀-䶵一-鿋豈-頻]')

def add_furigana(text, user_level=6):
    mode = tokenizer.SplitMode.C
    tokens = tokenizer.tokenize(text, mode)
    output = []

    """
    There are five steps to the logic that we need to solve here:
    1. Take the raw Japanese text, understanding it's a mix of Kanji and Kana.
    2. Break the string provided into individual morphemes -- we utilize Sudachi for this.
    3. For each morpheme, recognize if it contains Kanji characters and utilize a dictionary to find the yomi.
    4. Convert the yomi into Hiragana using pykakasi as it is provided in Katakana.
    5. Format the output to wrap the Kanji with furigana tags.
    """

    for t in tokens:
        surface = t.surface()
        if not KANJI_PATTERN.search(surface):
            output.append(surface)
            continue

        """
        Now that we've determined there is Kanji present, we check the word's N level in order to know whether
        or not to include furigana. We use Sudachi's dictionary form and check the JLPT level of the word. We
        do this using a yomitan JLPT vocab dictionary that makes use of Jonathan Waller's JLPT resources, similarly
        used by Jisho. It's most recent update is August 1st, 2025, and can be found here below.
        https://github.com/stephenmk/yomitan-jlpt-vocab
        """
        base_form = t.dictionary_form()
        word_level = JLPT_DICT.get(base_form)
        if word_level is not None and word_level >= user_level:
                output.append(surface)
                continue

        # Now that we've determined it's kanji that passes all the checks, we get to the slower parts of the code.
        readingKata = t.reading_form()
        conversion = kakasi.convert(readingKata)
        readingHira = "".join([i['hira'] for i in conversion])
        # Apparently, depending on pykakasi version, the below might fail if pykakasi breaks it into multiple parts.
        #readingHira = kakasi.convert(readingKata)[0]['hira']

        """
        We use difflib's SequenceMatcher to detect the direct differences between the Kanji (surface) and the pykakasi
        converted Hiragana (reading). In the case of full hiragana and/or particles, SequenceMatcher is skipped.

        get_opcodes gives instructions on how to change string 1 (surface) to string 2 (reading) via tag's values of
        "equal" or "replace". We use this to parse which parts of the surface actually need furigana and which don't.
        If parts are meant to be replaced (i.e. replace 返 in 返す with かえ) then the surface_out (返) will have
        the reading_out (かえ) above it.
        """

        if surface == readingHira:
                output.append(surface)
        else:
            s = SequenceMatcher(None, surface, readingHira)
            for tag, i1, i2, j1, j2 in s.get_opcodes():
                surface_out = surface[i1:i2]
                reading_out = readingHira[j1:j2]
                if tag == 'replace':
                    output.append(f"<ruby>{surface_out}<rt>{reading_out}</rt></ruby>")
                elif tag == 'equal':
                    output.append(surface_out)
    
    return "".join(output)

# Test!
"""
text = "「毎日、基礎的な練習を繰り返すことで、複雑な事柄も完璧に理解できます。」"
print(add_furigana(text, 3))
"""