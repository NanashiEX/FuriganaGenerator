from sudachipy import dictionary
import pykakasi

tokenizer = dictionary.Dictionary().create()
kakasi = pykakasi.kakasi()

def add_furigana(text):
    mode = tokenizer.SplitMode.C
    tokens = tokenizer.tokenize(text, mode)
    output = ""

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
        readingKata = t.reading_form()
        readingHira = kakasi.convert(readingKata)[0]['hira']

        if surface != readingHira:
            output += f"<ruby>{surface}<rt>{readingHira}</rt></ruby>"
        else:
            output += surface
    
    return output

# Test!
"""
text = "私は昨日新しい本を買いました"
print(add_furigana(text))
"""