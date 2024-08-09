# init_db.py

# =======================================
# ==============factoria.db==============
# =======================================

import sqlite3
import os

from game_api import get_all_items_info, get_recipe

def setup_database():
    print("===Initializing factoria.db===")
    # Check if the database file exists
    if os.path.exists('factoria.db'):
        print("Old factoria.db Found!")
        # Delete the existing database file
        os.remove('factoria.db')
        print("Deleted existing database 'factoria.db'.")
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
    print("Fetching Item Info!")
    items_info = get_all_items_info()
    # total_items_info = len(items_info)
    # Insert items into the items table
    for count, item in enumerate(items_info.values(), start=1):
        # print(f"Item Info Progress {count}/{total_items_info}")
        place_result = item.get('place_result', None)  # Use None if 'place_result' key is missing
        cursor.execute('''
        INSERT OR IGNORE INTO items (name, type, subgroup, stack_size, fuel_value, place_result, localised_name, localised_description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item['name'], item['type'], item['subgroup'], item['stack_size'], item['fuel_value'], place_result, str(item['localised_name']), str(item['localised_description'])))
    print("Item Info Fetched!")

    # Insert recipes into the recipes table
    print("Fetching Item Recipes!")
    for item_name in items_info.keys():
        recipe = get_recipe(item_name)
        if recipe:
            for ingredient in recipe['ingredients']:
                # Use a default value for result_count if it is missing
                result_count = recipe.get('result_count', 0)  # Default to 0 if result_count is not present
                cursor.execute('''
                INSERT INTO recipes (item_name, result_count, ingredient_name, ingredient_amount)
                VALUES (?, ?, ?, ?)
                ''', (recipe['item_name'], result_count, ingredient['name'], ingredient['amount']))
    print("Item Recipes Fetched!")

    # Commit and close connection
    conn.commit()
    conn.close()

    print("===factoria.db Initialized!===")
