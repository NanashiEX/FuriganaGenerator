import json
import zipfile
import re

yomitan_jlpt_path = r'C:\Users\koeng\Downloads\Yomitan\yomitan jlpt levels - jonathan waller.zip'

def create_jlpt_map(yomitan_jlpt_zip_path):
    jlpt_map = {}
    
    with zipfile.ZipFile(yomitan_jlpt_zip_path, 'r') as z:
        # Loop through every term_bank file in the zip
        for file_name in z.namelist():
            if file_name.startswith('term_meta_bank'):
                with z.open(file_name) as f:
                    data = json.load(f)
                    for entry in data:
                        word = entry[0]
                        
                        # 1. Access the metadata dictionary at index 2
                        meta_data = entry[2]
                        
                        # 2. Extract the "displayValue" (e.g., "N1")
                        # We use .get() to avoid errors if the keys are missing
                        display_val = meta_data.get("frequency", {}).get("displayValue", "")

                        # 3. Use regex to find the number in "N1", "N2", etc.
                        match = re.search(r'N([1-5])', display_val)
                        
                        if match:
                            level = int(match.group(1))

                            # 4. Keep the highest number (the "easiest" level)
                            # e.g., if a word is marked N2 and N3, we treat it as N3
                            if word not in jlpt_map or level > jlpt_map[word]:
                                jlpt_map[word] = level
                                
    # Save this to a small file (this will be around 1-2MB)
    with open('jlpt_lookup.json', 'w', encoding='utf-8') as f:
        json.dump(jlpt_map, f, ensure_ascii=False)

# Run this once on your machine
create_jlpt_map(yomitan_jlpt_path)