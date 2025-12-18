import streamlit as slit
from furigana import add_furigana

slit.set_page_config(
    page_title="Furigana Generator")
slit.title("Furigana Generator")
slit.markdown("""This tool utilizes SudachiPy for morphological analysis and pykakasi for converting readings to Hiragana.""")

input = slit.text_area("Enter Japanese text: ", value="テクストを入力してください。")

if slit.button("Generate Furigana"):
    if input.strip():
        with slit.spinner("Processing..."):
            result = add_furigana(input)

            slit.subheader("Result with Furigana:")
            slit.write(f"<div style='font-size: 24px; line-height: 2;'>{result}</div>", unsafe_allow_html=True)

            with slit.expander("View Raw HTML"):
                slit.code(result, language='html')
    else:
        slit.warning("Please enter some Japanese text to process.")
        

slit.divider()

slit.link_button("View Source Code", "https://github.com/Astrelle/FuriganaGenerator")
slit.caption("Build utilzing SudachiPy and pykakasi")

with slit.expander("Implementation Details"):
    slit.write("""
    - Tokenizer: SudachiPy for identifying compound morphemes.
    - Phonetics: pykakasi for Katakana to Hiragana normalization.
    - Visualization: HTML <ruby> tags for Furigana display.
    """)

