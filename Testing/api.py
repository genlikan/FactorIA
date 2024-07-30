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


def send_rcon_command(command):
    try:
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

def get_player_name():
    send_rcon_command('/get_player_name')
    json_data = read_file("player_name.json")
    print("==API== get_player_name:", json_data)
    return json_data

def get_inventory():
    """
    Retrieves the player's current inventory of items and the quantity.
    Returns:
        dict: A dictionary where the keys are item names (as strings) and the values are the quantities of those items (as integers).
    Example:
        {"burner-mining-drill":1,"stone-furnace":1,"wood":41,"coal":78,"stone":93,"iron-plate":8}
    """
    send_rcon_command('/get_inventory')
    json_data = read_file("player_inventory.json")
    # print("==API== RAW get_inventory:", json_data)
    # print(json.loads(json_data))
    return pretty_print_json(json_data)
    # player_inv = json.loads(json_data)
    # result = "The player has the following items in their inventory:\n"
    # print(player_inv)
    # for item in player_inv:
        # result += f"- {player_inv[item]} {item.replace('-', ' ')}\n"
        # print(item)
    # print(result)
    # return result
# print(get_inventory())
def get_all_items():
    """
    Retrieves a list of all possible item names in the game to search in recipes in json format.
    Returns:
        list: A list of strings where each string is the name of an item available in the game.
    Example:
        ["burner-mining-drill", "stone-furnace", "wood", "coal", "stone", "iron-plate", "copper-plate", "steel-plate", "iron-gear-wheel", "electronic-circuit"]
    """
    send_rcon_command('/get_all_items')
    json_data = read_file("all_items.json")
    # print("==API== RAW get_all_items:", json_data)
    return pretty_print_json(json_data)

# print(get_all_items())

def get_all_items_info():
    send_rcon_command('/get_all_items_info')
    json_data = read_file("all_items_info.json")
    return pretty_print_json(json_data)


# print(get_all_items_info())

def get_recipe(item_name: str):
    """Get the recipe required to craft a given item. Please reference get_all_items() for item names. Input cannot be blank.
    
    Args:
        item_name (str): The name of the item with spaces seperated by '-'.
        
    Returns:
        dict: A dictionary containing the item's "type", the item's name that is required to craft it "name", and "amount" required to craft one.
    """
    item_name = item_name.replace(" ", "-")
    send_rcon_command(f'/get_recipe {item_name.lower()}')
    json_data = read_file("recipe.json")
    # recipe_info = json.loads(json_data)
    # print(recipe_info)
    # print("To make:", item_name)
    # result = f" One {item_name} requires the following:\n"
    # print("You will need:",recipe_info[0]["amount"], recipe_info[0]['name'])
    # for items in recipe_info:
    #     print(items["amount"], items["name"])
    # for item in recipe_info:
    #     result += f"- {item['amount']} {item['name'].replace('-', ' ')}\n"
    #     # print(item)
    # print(result)
    # return result
    # print("==API== RAW get_recipe:", json_data)
    return pretty_print_json(json_data)

# print(get_recipe("inserter"))
# print(get_recipe("wooden-chest"))


def get_technologies():
    """Get the player's researched technologies.
    
    Returns:
        dict: A dictionary containing the player's researched technologies.
    """
    send_rcon_command('/get_technologies')
    json_data = read_file("technologies.json")
    return pretty_print_json(json_data)

def get_technology_info(tech_name: str):
    """Get the technology information for a given technology.

    Args:
        tech_name (str): The name of the technology.

    Returns:
        dict: A dictionary containing the information for the technology.
    """
    send_rcon_command(f'/get_technology_info {tech_name}')
    json_data = read_file("technology_info.json")
    return pretty_print_json(json_data)

def get_all_technologies():
    """Get all available technology in the game.

    Returns:
        dict: A dictionary containing the all technologies available in the game.
    """
    send_rcon_command('/get_all_technologies')
    json_data = read_file("all_technologies.json")
    return pretty_print_json(json_data)

# @lru_cache(maxsize=128)
# def get_cached_inventory():
#     return get_inventory()

@lru_cache(maxsize=128)
def get_cached_recipe(item_name):
    return get_recipe(item_name)

# @lru_cache(maxsize=128)
# def get_cached_technologies():
#     return get_technologies()

# @lru_cache(maxsize=128)
# def get_cached_technology_info(technology_name):
#     return get_technology_info(technology_name)

@lru_cache(maxsize=1)
def get_cached_all_technologies():
    return get_all_technologies()

