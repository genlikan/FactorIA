import json
import os

def load_localization_files(directory):
    localization = {}
    for filename in os.listdir(directory):
        if filename.endswith(".cfg"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                section = None
                for line in file:
                    line = line.strip()
                    if line.startswith('[') and line.endswith(']'):
                        section = line[1:-1]
                        localization[section] = localization.get(section, {})
                    elif section and '=' in line:
                        key, value = map(str.strip, line.split('=', 1))
                        localization[section][key] = value
    return localization

# Adjust the path to your Factorio localization folder
localization_directory = "C:/Program Files (x86)/Steam/steamapps/common/Factorio/data/base/locale/en"
localization_data = load_localization_files(localization_directory)

# Write the localization data to a JSON file
with open('localization_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(localization_data, json_file, ensure_ascii=False, indent=4)
