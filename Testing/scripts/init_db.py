# init_db.py

# =======================================
# ==============factoria.db==============
# =======================================

import sqlite3

from test_api import get_all_items, get_all_items_info, get_inventory, get_recipe

# Connect to SQLite database (or create it)
conn = sqlite3.connect('factoria.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    name TEXT PRIMARY KEY,
    type TEXT,
    subgroup TEXT,
    stack_size INTEGER,
    fuel_value INTEGER,
    place_result TEXT,
    localised_name TEXT,
    localised_description TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recipes (
    item_name TEXT,
    result_count INTEGER,
    ingredient_name TEXT,
    ingredient_amount INTEGER,
    FOREIGN KEY(item_name) REFERENCES items(name)
)
''')

# Fetch all items info
items_info = get_all_items_info()

# Insert items into the items table
for item in items_info.values():
    place_result = item.get('place_result', None)  # Use None if 'place_result' key is missing
    cursor.execute('''
    INSERT OR IGNORE INTO items (name, type, subgroup, stack_size, fuel_value, place_result, localised_name, localised_description)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (item['name'], item['type'], item['subgroup'], item['stack_size'], item['fuel_value'], place_result, str(item['localised_name']), str(item['localised_description'])))

# Insert recipes into the recipes table
for item_name in items_info.keys():
    recipe = get_recipe(item_name)
    if recipe:
        for ingredient in recipe['ingredients']:
            cursor.execute('''
            INSERT INTO recipes (item_name, result_count, ingredient_name, ingredient_amount)
            VALUES (?, ?, ?, ?)
            ''', (recipe['item_name'], recipe['result_count'], ingredient['name'], ingredient['amount']))

# Commit and close connection
conn.commit()
conn.close()
