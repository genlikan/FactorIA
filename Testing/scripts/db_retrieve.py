import sqlite3

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