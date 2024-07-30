import os
import json
from mcrcon import MCRcon
RCON_HOST = "localhost"
RCON_PORT = 25575
RCON_PASSWORD = "your_password"
# OUTPUT_DIR = "../../script-output"
OUTPUT_DIR = os.getenv('APPDATA') + "/Factorio/script-output"


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

def get_all_items(debug=False):
    send_rcon_command('/get_all_items', debug)
    json_data = read_file("all_items.json")
    return json.loads(json_data)

def get_all_items_info(debug=False):
    send_rcon_command('/get_all_items_info', debug)
    json_data = read_file("all_items_info.json")
    return json.loads(json_data)

def get_inventory(debug=False):
    send_rcon_command('/get_inventory', debug)
    json_data = read_file("player_inventory.json")
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

# ====Example Usage====
# get_all_items(debug=True)
# get_all_items_info(debug=True)
# get_inventory(debug=True)
# get_recipe("inserter",debug=True)
