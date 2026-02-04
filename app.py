import streamlit as slit
from furigana import add_furigana

slit.set_page_config(
    page_title="Furigana Generator")
slit.title("Furigana Generator")
slit.markdown("""This tool utilizes SudachiPy for morphological analysis and pykakasi for converting readings to Hiragana.""")

# 1. Create a dictionary to map UI labels to numbers
# We include "Show All" as level 6 (because no word is level 6 or higher, so nothing gets skipped)
jlpt_options = {"N1": 1, "N2": 2, "N3": 3, "N4": 4, "N5": 5, "Show All": 6}

# 2. Add the selection UI
# Using columns to put the label and the selector on the same line
col1, col2 = slit.columns([1, 4])
with col1:
    slit.write("**Hide up to:**")
with col2:
    selected_label = slit.radio(
        "Select JLPT Level",
        options=list(jlpt_options.keys()),
        index=5, # Default to "Show All"
        horizontal=True,
        label_visibility="collapsed"
    )

selected_level = jlpt_options[selected_label]

input = slit.text_area("Enter Japanese text: ", value="テクストを入力してください。")

if slit.button("Generate Furigana"):
    if input.strip():
        with slit.spinner("Processing..."):
            # 3. Pass the selected level into your function
            result = add_furigana(input, user_level=selected_level)

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

