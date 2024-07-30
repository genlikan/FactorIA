from model import generate_response
# from todo import setup_database
# from reminder import start_reminder_thread
from api import get_player_name

def main():
    # setup_database()
    # start_reminder_thread()
    try:
        player_name = get_player_name()
        print(f"Greetings {player_name}!")
        pass
    except:
        print("Game not Launched")
    while True:
        user_query = input("Ask your Factorio assistant: ")
        print(f"=== Query Get ===:  {user_query}")
        response = generate_response(user_query)
        print(f"=== Response ===: {response}")
        # print(f"=== Player Response ===: \n{response[0]['arguments']['content']}")

if __name__ == "__main__":
    main()
