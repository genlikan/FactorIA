from db_retrieve import get_recipe_from_db, get_subgroup_from_db, list_all_item_names_from_db, find_closest_item_name_from_db
from game_api import get_player_name, get_inventory, get_all_items, get_all_items_info, get_recipe, get_technologies, get_technology_info, get_all_technologies



def can_craft(item_name, inventory, count):
    recipe = get_recipe_from_db(item_name)
    if not recipe:
        return False, {}

    needed_items = {}
    for ingredient in recipe['ingredients']:
        needed_amount = ingredient['amount'] * count
        if inventory.get(ingredient['name'], 0) < needed_amount:
            subgroup = get_subgroup_from_db(ingredient['name'])
            if subgroup == 'raw-material':
                needed_items[ingredient['name']] = needed_amount - inventory.get(ingredient['name'], 0)
                return False, needed_items
            needed_items[ingredient['name']] = needed_amount - inventory.get(ingredient['name'], 0)
    
    for needed_item, needed_amount in needed_items.items():
        can_craft_needed, missing_items = can_craft(needed_item, inventory, needed_amount)
        if not can_craft_needed:
            needed_items.update(missing_items)
            return False, needed_items
    
    return True, {}

def craft(item_name, inventory, count):
    recipe = get_recipe_from_db(item_name)
    if not recipe:
        return False

    for ingredient in recipe['ingredients']:
        needed_amount = ingredient['amount'] * count
        if inventory.get(ingredient['name'], 0) < needed_amount:
            required_count = needed_amount - inventory.get(ingredient['name'], 0)
            subgroup = get_subgroup_from_db(ingredient['name'])
            if subgroup == 'raw-material':
                return False
            can_craft_needed, missing_items = can_craft(ingredient['name'], inventory, required_count)
            if not can_craft_needed:
                return False
            if not craft(ingredient['name'], inventory, required_count):
                return False
        inventory[ingredient['name']] -= needed_amount
    
    if item_name in inventory:
        inventory[item_name] += recipe['result_count'] * count
    else:
        inventory[item_name] = recipe['result_count'] * count
    return True

def calculate_max_items(item_name: str):
    """
    Calculates how many the player can craft for a particular item_name.
    Args:
        item_name(str): the item name to calculate how many the player can craft.
    Returns:
        str: A string describing the crafting result.
    """
    # item_name = item_name.lower().replace(" ", "-")
    item_name = find_closest_item_name_from_db(item_name)

    inventory = get_inventory()
    max_items = 0
    total_produced = 0

    can_craft_needed, missing_items = can_craft(item_name, inventory, 1)
    if not can_craft_needed:
        missing_items_str = ', '.join([f"{item}: {amount}" for item, amount in missing_items.items()])
        return f"Cannot craft {item_name} due to missing items: {missing_items_str}"

    while can_craft_needed:
        if not craft(item_name, inventory, 1):
            break
        max_items += 1
        total_produced += get_recipe_from_db(item_name)['result_count']
        can_craft_needed, missing_items = can_craft(item_name, inventory, 1)

    if max_items == total_produced:
        return f"Maximum {item_name}s that can be made with current player inventory: {max_items}"
    else:
        return f"Maximum {item_name}s that can be made: {max_items} with a total of {total_produced}"

# print(calculate_max_items("gun-turret"))
# ============================================================

def can_theoretically_craft(item_name, inventory, count):
    recipe = get_recipe_from_db(item_name)
    if not recipe:
        return False, {}

    needed_items = {}
    for ingredient in recipe['ingredients']:
        needed_amount = ingredient['amount'] * count
        if inventory.get(ingredient['name'], 0) < needed_amount:
            subgroup = get_subgroup_from_db(ingredient['name'])
            if subgroup == 'raw-material':
                needed_items[ingredient['name']] = needed_amount - inventory.get(ingredient['name'], 0)
            else:
                needed_items[ingredient['name']] = needed_amount - inventory.get(ingredient['name'], 0)
                can_craft_needed, missing_items = can_craft(ingredient['name'], inventory, needed_items[ingredient['name']])
                if not can_craft_needed:
                    needed_items.update(missing_items)
    
    if needed_items:
        return False, needed_items
    return True, {}

def theoretical_requirements(item_name: str, count: int):
    """
    Calculates the theoretical requirements to craft a certain number of items.
    Args:
        item_name(str): the item name to calculate requirements for.
        count(int): the number of items to craft.
    Returns:
        str: A string describing the missing items required.
    """
    item_name = find_closest_item_name_from_db(item_name)
    # item_name = item_name.lower().replace(" ", "-")
    inventory = get_inventory()

    can_craft_needed, missing_items = can_theoretically_craft(item_name, inventory, count)
    if can_craft_needed:
        return f"You can craft {count} {item_name}(s) with the current inventory."
    else:
        missing_items_str = ', '.join([f"{item}: {amount}" for item, amount in missing_items.items()])
        return f"To craft {count} {item_name}(s), you need: {missing_items_str}"

# print(theoretical_requirements("laser-turret",12))

def find_closest_item_name(item_name: str):
    """
    Find the closest name to the item_name from the list of item names in the game.

    Args:
        item_name (str): The name to find the closest match for.

    Returns:
        str: The closest name found in the game.
    """
    return find_closest_item_name_from_db(item_name)


# print(calculate_max_items("power-armor"))
# print(calculate_max_items("laser-turret"))
# print(calculate_max_items("pipe"))
# print(calculate_max_items("pipe"))

# # =====LIST ALL ITEMS THAT CAN BE CRAFTED=====

# items_with_recipes = []

# for item in get_all_items():
#     if get_recipe_from_db(item) is not None:
#         items_with_recipes.append(item)

# inventory = get_inventory()
# for item in items_with_recipes:
#     print(calculate_max_items(item))
# ============================================================

    # max_items, total_produced = calculate_max_items(item, inventory.copy())
    # if max_items != 0:
    #     if max_items == total_produced:
    #         print(f"Maximum {item}s that can be made: {max_items}")
    #     else:
    #         print(f"Maximum {item}s that can be made: {max_items} with a total of {total_produced}")

# ============================================================

def get_player_inventory():
    """
    Returns the players inventory in dict format.
    """
    return get_inventory()

def get_item_recipe(item_name: str):
    """
    Returns the recipe for a given item_name in dict format.

    Args:
        item_name (str): The name of the item to search the recipe for. 
                         Must not be empty.

    Returns:
        dict: The recipe for the item.

    Raises:
        ValueError: If item_name is empty.
    """
    if not item_name:
        raise ValueError("item_name cannot be empty.")
    # Replace spaces with hyphens
    item_name = item_name.replace(" ", "-")
    
    return get_recipe_from_db(item_name)

# print(get_item_recipe("wooden-chest"))

def get_all_item_names():
    """
    List all in-game item names in the game.

    Args:
        db_name (str): The name of the database file.

    Returns:
        list: A list of item names.
    """
    return list_all_item_names_from_db()
