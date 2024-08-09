import timeit
import random

from init_db import setup_database
from game_api import get_player_name, get_inventory, get_all_items, get_all_items_info, get_recipe
from db_retrieve import get_recipe_from_db,list_all_item_names_from_db

calls = 1000

# =======Database=======
print("==Start setup_database()==")
execution_time = timeit.timeit("setup_database()", globals=globals(), number=1)
print(f"Execution time for 1 call: {execution_time} seconds")

# =======Player Info=======

print("==Start get_player_name()==")
execution_time = timeit.timeit("get_player_name()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

print("==Start get_inventory()==")
execution_time = timeit.timeit("get_inventory()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

# =========Game Items=========

print("==Start get_all_items()==")
execution_time = timeit.timeit("get_all_items()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

print("==Start list_all_item_names_from_db()==")
execution_time = timeit.timeit("list_all_item_names_from_db()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

print("==Start get_all_items_info()==")
execution_time = timeit.timeit("get_all_items_info()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

# =========Game Recipes=========
all_item_names_from_db = list_all_item_names_from_db()

def wrapper():
    item_name = random.choice(all_item_names_from_db)
    get_recipe(item_name)

print("==Start get_recipe(item_name)==")
execution_time = timeit.timeit(wrapper, number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

def db_wrapper():
    item_name = random.choice(all_item_names_from_db)
    get_recipe_from_db(item_name)

print("==Start get_recipe_from_db(item_name)==")
execution_time = timeit.timeit(db_wrapper, number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")
