import os
import time
import json
from mcrcon import MCRcon
from functools import lru_cache

RCON_HOST = "localhost"
RCON_PORT = 25575
RCON_PASSWORD = "your_password"
# OUTPUT_DIR = "../../script-output"
OUTPUT_DIR = os.getenv('APPDATA') + "/Factorio/script-output"

# ====================================

def send_rcon_command(command, debug=False):
    try:
        if debug:
            print("==API== Attempting Sending of command:", command)
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            mcr.command(command)
    except Exception as e:
        print(f"Failed to send command: {e}")

def read_file(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    while not os.path.exists(filepath):
        time.sleep(0.1)
    with open(filepath, "r") as file:
        return file.read()

def pretty_print_json(json_string):
    try:
        data = json.loads(json_string)
        return json.dumps(data, indent=4)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return json_string

# =======Player Info===========

def get_player_name(debug=False):
    send_rcon_command('/get_player_name', debug)
    json_data = read_file("player_name.json")
    print("==API== get_player_name:", json_data)
    return json_data

def get_inventory(debug=False):
    send_rcon_command('/get_inventory', debug)
    json_data = read_file("player_inventory.json")
    return json.loads(json_data)

# =========Game Items============

def get_all_items(debug=False):
    send_rcon_command('/get_all_items', debug)
    json_data = read_file("all_items.json")
    return json.loads(json_data)

def get_all_items_info(debug=False):
    send_rcon_command('/get_all_items_info', debug)
    json_data = read_file("all_items_info.json")
    return json.loads(json_data)

def get_recipe(item_name: str, debug=False):
    item_name = item_name.replace(" ", "-")
    send_rcon_command(f'/get_recipe {item_name.lower()}', debug)
    json_data = read_file("recipe.json")
    try:
        recipe_dict = json.loads(json_data)
    except:
        return None
    return recipe_dict

# =========Game Technologies============

def get_technologies(debug=False):
    send_rcon_command('/get_technologies', debug)
    json_data = read_file("technologies.json")
    return json.loads(json_data)

def get_technology_info(tech_name: str, debug=False):
    send_rcon_command(f'/get_technology_info {tech_name}', debug)
    json_data = read_file("technology_info.json")
    return json.loads(json_data)

def get_all_technologies(debug=False):
    send_rcon_command('/get_all_technologies', debug)
    json_data = read_file("all_technologies.json")
    return json.loads(json_data)


# =======Player Info===========
# print(get_player_name(debug=True))
# print(get_inventory(debug=True))

# =========Game Items============
# print(get_all_items(debug=True))
# print(get_all_items_info(debug=True))
# print(get_recipe("inserter",debug=True))

# =========Game Technologies============
# print(get_technologies(debug=True))
# print(get_technology_info("fusion-reactor-equipment",debug=True))
# print(get_all_technologies(debug=True))

