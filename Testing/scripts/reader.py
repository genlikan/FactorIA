import json
import time
import os

file_path = "player_inventory.json"

def read_inventory():
    try:
        with open(file_path, 'r') as file:
            inventory_data = json.load(file)
            return inventory_data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def main():
    while True:
        inventory_data = read_inventory()
        if inventory_data:
            print("Player Inventory:", inventory_data)
        else:
            print("No data available or file not found.")
        
        time.sleep(20)  # Adjust the interval as needed

if __name__ == "__main__":
    main()


# inventory_data = read_inventory()

# # for item in inventory_data:
#     # print(item["name"], ":", item["count"])

# def item_sum(itemname):
#     total_count =  sum(item['count'] for item in inventory_data if item['name'] == itemname)
#     return total_count

# print(f"Total amount of wood: {item_sum('wood')}")