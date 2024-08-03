# def get_inventory():
#     return {'transport-belt': 200, 'fast-transport-belt': 120, 'fast-underground-belt': 88, 'fast-splitter': 42, 'inserter': 237, 'long-handed-inserter': 24, 'fast-inserter': 332, 'small-electric-pole': 29, 'medium-electric-pole': 3, 'big-electric-pole': 5, 'substation': 2, 'pipe': 1, 'pipe-to-ground': 32, 'rail': 225, 'car': 1, 'construction-robot': 15, 'concrete': 800, 'repair-pack': 19, 'accumulator': 40, 'heat-exchanger': 4, 'electric-mining-drill': 32, 'stone-furnace': 13, 'electric-furnace': 67, 'assembling-machine-2': 91, 'wood': 163, 'coal': 62, 'raw-fish': 6, 'iron-plate': 466, 'copper-plate': 623, 'steel-plate': 612, 'plastic-bar': 111, 'battery': 4, 'electronic-circuit': 267, 'advanced-circuit': 58, 'processing-unit': 95, 'engine-unit': 89, 'electric-engine-unit': 5, 'uranium-fuel-cell': 8, 'piercing-rounds-magazine': 90, 'stone-wall': 745, 'gate': 3, 'gun-turret': 1, 'laser-turret': 104}

# def get_recipe_from_db(item_name):
#     recipes = {
#         'inserter': {'result_count': 1, 'ingredients': [{'name': 'iron-plate', 'amount': 1}, {'name': 'iron-gear-wheel', 'amount': 1}, {'name': 'electronic-circuit', 'amount': 1}]},
#         'iron-gear-wheel': {'result_count': 1, 'ingredients': [{'name': 'iron-plate', 'amount': 2}]},
#         'electronic-circuit': {'result_count': 1, 'ingredients': [{'name': 'iron-plate', 'amount': 1}, {'name': 'copper-cable', 'amount': 3}]},
#         'copper-cable': {'result_count': 2, 'ingredients': [{'name': 'copper-plate', 'amount': 1}]},
#         'fast-splitter': {'result_count': 1, 'ingredients': [{'name': 'iron-gear-wheel', 'amount': 10}, {'name': 'electronic-circuit', 'amount': 10}, {'name': 'splitter', 'amount': 1}]},
#         'fast-inserter': {'result_count': 1, 'ingredients': [{'name': 'iron-plate', 'amount': 2}, {'name': 'electronic-circuit', 'amount': 2}, {'name': 'inserter', 'amount': 1}]},
#         'splitter': {'result_count': 1, 'ingredients': [{'name': 'iron-plate', 'amount': 5}, {'name': 'transport-belt', 'amount': 5}, {'name': 'electronic-circuit', 'amount': 5}]},
#         'transport-belt': {'result_count': 2, 'ingredients': [{'name': 'iron-plate', 'amount': 1}, {'name': 'iron-gear-wheel', 'amount': 1}]}
#     }
#     return recipes.get(item_name, None)

# from test_api import get_inventory
from db_retrieve import get_recipe_from_db, get_subgroup_from_db
from test_api import get_all_items, get_all_items_info, get_inventory

# print(get_recipe_from_db("inserter"))
# print(get_recipe_from_db("iron-gear-wheel"))
# print(get_recipe_from_db("iron-plate"))
# print(get_recipe_from_db("iron-ore"))
# print(get_recipe_from_db("electronic-circuit"))
# print(get_recipe_from_db("copper-cable"))
# print(get_recipe_from_db("copper-plate"))
# print(get_recipe_from_db("copper-ore"))


def get_unique_items(item_name):
    unique_items = set()

    def find_unique_items(item):
        if item not in unique_items:
            unique_items.add(item)
            recipe = get_recipe_from_db(item)
            if recipe and 'ingredients' in recipe:
                for ingredient in recipe['ingredients']:
                    find_unique_items(ingredient['name'])

    find_unique_items(item_name)
    return list(unique_items)

# Example usage
# unique_items = get_unique_items("inserter")
# print(unique_items)

# for item in get_unique_items("inserter"):
    # print(f"==={item}===")
    # print(get_recipe_from_db(item))

# print(get_inventory())

# print(get_recipe_from_db("inserter"))

# def craft_inserters(item_name):
#     # Fetch inventory and recipe
#     inventory = get_inventory()
#     recipe = get_recipe_from_db(item_name)
    
#     if not recipe:
#         raise ValueError(f"No recipe found for item: {item_name}")
    
#     # Determine the maximum number of inserters that can be crafted
#     max_inserters = min(inventory[ingredient['name']] // ingredient['amount'] for ingredient in recipe['ingredients'])
    
#     # Update the inventory based on the number of inserters crafted
#     for ingredient in recipe['ingredients']:
#         inventory[ingredient['name']] -= max_inserters * ingredient['amount']
    
#     return inventory

# # Calculate remaining inventory after crafting inserters
# remaining_inventory = craft_inserters('inserter')
# print(remaining_inventory)

# print(len(get_all_items()))



# print(items_with_recipes)
# print(len(items_with_recipes))

def can_craft(item_name, inventory, count):
    recipe = get_recipe_from_db(item_name)
    if not recipe:
        return False

    needed_items = {}
    for ingredient in recipe['ingredients']:
        needed_amount = ingredient['amount'] * count
        if inventory.get(ingredient['name'], 0) < needed_amount:
            subgroup = get_subgroup_from_db(ingredient['name'])
            if subgroup == 'raw-material':
                return False
            needed_items[ingredient['name']] = needed_amount - inventory.get(ingredient['name'], 0)
    
    for needed_item, needed_amount in needed_items.items():
        if not can_craft(needed_item, inventory, needed_amount):
            return False
    
    return True

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
            if not can_craft(ingredient['name'], inventory, required_count):
                return False
            if not craft(ingredient['name'], inventory, required_count):
                return False
        inventory[ingredient['name']] -= needed_amount
    
    if item_name in inventory:
        inventory[item_name] += recipe['result_count'] * count
    else:
        inventory[item_name] = recipe['result_count'] * count
    return True

def calculate_max_items(item_name, inventory):
    max_items = 0
    total_produced = 0
    while can_craft(item_name, inventory, 1):
        if not craft(item_name, inventory, 1):
            break
        max_items += 1
        total_produced += get_recipe_from_db(item_name)['result_count']
    return max_items, total_produced

# Example usage
# inventory = get_inventory()
# print(inventory)
# item_to_craft = 'fast-splitter'
# max_items = calculate_max_items(item_to_craft, inventory)

# print(f"Maximum {item_to_craft}s that can be made: {max_items}")
# print("Remaining inventory after crafting:")
# print(inventory)

# =====LIST ALL ITEMS THAT CAN BE CRAFTED=====

items_with_recipes = []

for item in get_all_items():
    if get_recipe_from_db(item) is not None:
        items_with_recipes.append(item)

# inventory = get_inventory()
# for item in items_with_recipes:
#     max_items, total_produced = calculate_max_items(item, inventory.copy())
#     if max_items != 0:
#         if max_items == total_produced:
#             print(f"Maximum {item}s that can be made: {max_items}")
#         else:
#             print(f"Maximum {item}s that can be made: {max_items} with a total of {total_produced}")

# =====LIST ALL ITEMS THAT CAN BE CRAFTED=====

# print(get_recipe_from_db("transport-belt"))
# print(get_all_items_info())

# all_info_dict = get_all_items_info()

# print(all_info_dict)

# def print_raw_material_details(items_info):
#     count = 0
#     for item_name, item_details in items_info.items():
#         if item_details.get('subgroup') == 'raw-material':
#             count += 1
#             print(item_details)
#     print(count)
# print(print_raw_material_details(all_info_dict))

# =============
print(items_with_recipes)