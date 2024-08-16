import time
from model import generate_response
from game_api import get_player_name
from init_db import setup_database

def main():
    setup_database()
    try:
        player_name = get_player_name()
        print(f"Greetings {player_name}!")
        pass
    except:
        print("Game not Launched")
    while True:
        user_query = input("Ask your Factorio assistant: ")
        print(f"=== Query Get ===:  {user_query}")
        start_time = time.time()
        response = generate_response(user_query)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken to receive response: {elapsed_time:.4f} seconds")
        print(f"=== Response ===: {response}")
        # print(f"=== Player Response ===: \n{response[0]['arguments']['content']}")

if __name__ == "__main__":
    main()