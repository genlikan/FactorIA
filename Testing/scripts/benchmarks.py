import timeit
import random

from test_api import get_all_items, get_all_items_info, get_inventory, get_recipe
from db_retrieve import get_recipe_from_db


all_item_names = get_all_items()


calls = 1000

print("==Start get_all_items()==")
execution_time = timeit.timeit("get_all_items()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

print("==Start get_all_items_info()==")
execution_time = timeit.timeit("get_all_items_info()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

print("==Start get_inventory()==")
execution_time = timeit.timeit("get_inventory()", globals=globals(), number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

def wrapper():
    item_name = random.choice(all_item_names)
    get_recipe(item_name)

print("==Start get_recipe(item_name)==")
execution_time = timeit.timeit(wrapper, number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")

def db_wrapper():
    item_name = random.choice(all_item_names)
    get_recipe_from_db(item_name)

print("==Start get_recipe_from_db(item_name)==")
execution_time = timeit.timeit(db_wrapper, number=calls)
print(f"Execution time for {calls} calls: {execution_time} seconds")
