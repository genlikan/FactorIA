import sqlite3
from difflib import get_close_matches

def get_recipe_from_db(item_name: str):
    # Connect to SQLite database
    conn = sqlite3.connect('factoria.db')
    cursor = conn.cursor()

    # Query to retrieve the recipe for the specified item
    cursor.execute('''
    SELECT r.item_name, r.result_count, r.ingredient_name, r.ingredient_amount
    FROM recipes r
    JOIN items i ON r.item_name = i.name
    WHERE r.item_name = ?
    ''', (item_name,))

    # Fetch all results
    recipe = cursor.fetchall()

    # Close the connection
    conn.close()

    # Process and return the recipe in a readable format
    if recipe:
        result = {
            "item_name": recipe[0][0],
            "result_count": recipe[0][1],
            "ingredients": [{"name": row[2], "amount": row[3]} for row in recipe]
        }
        return result
    else:
        return None

def format_recipe(recipe):
    if not recipe:
        return "No recipe found for the specified item."

    item_name = recipe['item_name']
    result_count = recipe['result_count']
    ingredients = recipe['ingredients']

    formatted_ingredients = '\n'.join([f" - {ingredient['amount']} x {ingredient['name']}" for ingredient in ingredients])

    return f"Recipe for {item_name} (produces {result_count}):\n{formatted_ingredients}"


def get_subgroup_from_db(item_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('factoria.db')
    cursor = conn.cursor()
    
    # Query to retrieve the subgroup for the given item name
    cursor.execute('SELECT subgroup FROM items WHERE name = ?', (item_name,))
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    if result:
        return result[0]  # Return the subgroup
    else:
        return None  # Return None if the item was not found

def list_all_item_names_from_db():
    """
    List all item names in the 'items'.

    Returns:
        list: A list of item names.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('factoria.db')
    cursor = conn.cursor()

    # Execute the query to fetch all item names
    cursor.execute("SELECT name FROM items")

    # Retrieve all results
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Extract item names from the rows and return them as a list
    item_names = [row[0] for row in rows]
    return item_names

def find_closest_item_name_from_db(input_name):
    """
    Find the closest name to the input_name from the list of item names in the database.

    Args:
        input_name (str): The name to find the closest match for.

    Returns:
        str: The closest name found in the database.
    """
    item_names = list_all_item_names_from_db()
    closest_matches = get_close_matches(input_name, item_names, n=1, cutoff=0.6)
    
    if closest_matches:
        return closest_matches[0]
    else:
        return None

# Example usage:
# input_name = "burner turbine "
# closest_name = find_closest_item_name_from_db(input_name)
# if closest_name:
#     print(f"The closest name to '{input_name}' is '{closest_name}'.")
#     print(get_recipe_from_db(closest_name))
# else:
#     print(f"No close match found for '{input_name}'.")

# # Example usage
# item_name = 'iron-plate'
# subgroup = get_subgroup_from_db(item_name)
# if subgroup:
#     print(f"The subgroup of {item_name} is {subgroup}.")
# else:
#     print(f"{item_name} not found in the database.")

# Example usage
# item_name = "inserter"  # Replace with any item name you want to retrieve the recipe for
# recipe = get_recipe_from_db(item_name)
# print(recipe)
# formatted_recipe = format_recipe(recipe)
# print(formatted_recipe)

# print(get_recipe_from_db("inserter"))
# print(get_recipe_from_db("iron-gear-wheel"))
# print(get_recipe_from_db("electronic-circuit"))
# print(get_recipe_from_db("copper-cable"))