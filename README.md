# Furigana Generator

Live Demo: https://furiganagenerator.streamlit.app/

NLP web application written in Python 3.13 to generate Furigana for Japanese text. This project utilizes morphological analysis to handle Kanji-Kana orthography.

# Tools Utilized

* [SudachiPy](https://github.com/WorksApplications/SudachiPy) - Morphological Tokenization
* [pykakasi](https://github.com/miurahr/pykakasi) - Normalizing Katakana to Hiragana.
* [Streamlit](https://streamlit.io/) - Deployment, WebUI


# Installation & Usage

1. Clone the repository
```git clone https://github.com/Astrelle/FuriganaGenerator.git```

2. Install dependencies
```pip install -r requirements.txt```

3. Run the application
```streamlit run app.py```

# Roadmap

Currently, this Furigana generator is extremely lacking and primarily served to understand the tools utilized. However, that does not mean there aren't plans to improve the tool.

[ ] Okurigana Exclusion - Remove furigana from the kana characters trailing behind a kanji stem.

[ ] JLPT Vocabulary Filtering - Filter furigana visibility based on level of vocabulary regarding the JLPT to reduce visual noise.
