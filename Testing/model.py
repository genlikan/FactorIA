import os
from llama_cpp import Llama
from llama_cpp_agent import LlamaCppFunctionTool, FunctionCallingAgent, MessagesFormatterType
from llama_cpp_agent.providers import LlamaCppPythonProvider
from llama_cpp_agent.chat_history import BasicChatHistory, BasicChatMessageStore, BasicChatHistoryStrategy
from model_tools import get_player_inventory, calculate_max_items, find_closest_item_name, theoretical_requirements
# from todo import add_todo_item, get_todo_list, update_todo_status
# from retriever import Retriever

# Load pre-trained model
# model_path = os.getenv("USERPROFILE") + "/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q3_K_L.gguf"
model_path = os.getenv("USERPROFILE") + "/.cache/lm-studio/models/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/Meta-Llama-3.1-8B-Instruct-Q8_0.gguf"

llm = Llama(
    model_path=model_path, 
    chat_format="llama-3",
    n_gpu_layers=-1,
    #################
    use_mlock = True,
    # n_threads = 4,
    # n_batch=512,
    # n_predict = -1,
    seed = 400,
    # batch_size=16,
    # threads=8,
    verbose=False,
    # n_ctx=2048,       # /4
    # n_ctx=4096,       # /2
    # n_ctx=8192,       # Default
    # n_ctx=16384,      # x2
    n_ctx=32768,      # x4
    # n_ctx=49152,      # x6
    # n_ctx=57344,      # x7
    # n_ctx=65536,      # x8 - MAX before performance hit - Preferred for RTX 3090
    # n_ctx=73728,      # x9- VRam Limit
    # n_ctx=81920,      # x10 
    # n_ctx=98304,      # x12
    # n_ctx=131072      # x16 - Model Max
)

# Set up the provider
provider = LlamaCppPythonProvider(llm)

# Create a message store for the chat history
chat_history_store = BasicChatMessageStore()

# Create the actual chat history, by passing the wished chat history strategy, it can be last_k_message or last_k_tokens. The default strategy will be to use the 20 last messages for the chat history.
# We will use the last_k_tokens strategy which will include the last k tokens into the chat history. When we use this strategy, we will have to pass the provider to the class.
chat_history = BasicChatHistory(
    message_store=chat_history_store, 
    chat_history_strategy=BasicChatHistoryStrategy.last_k_tokens, 
    k=70000, 
    llm_provider=provider
)

# System prompt to guide the model's responses
system_prompt = """
    You are a smart and helpful gaming helper for the game Factorio. You provide accurate and concise information, about the game and anything else. 
    You can retrieve player inventory via get_player_inventory, find_closest_item_name, theoretical_requirements, or calculate_max_items in the game.
    The player may misspell some items, please use the function find_closest_item_name to check for the nearest item name the player may be referring to.
    You must help the player to the best of your abilities.
    The player may ask what they have in their inventory, use the function get_player_inventory to get that information. 
    If the player asks for how much of an item they can craft, please use the function calculate_max_items(item_name), this function already considers the player's inventory, so you will not need to use the player inventory function, and will have information about what else the player may need.
    The player may ask hypothetically what they would need to craft some amount of items, inform the player what they need with the theoretical_requirements function.
    If the player doesn't have enough to make the item, be exact and explain to the player the exact amount of what else do they need and how much.
    The player may ask general questions that do not need any function calls, please answer them to the best of your knowledge anyways.
    When responding back to the player, be sure to answer with natural language, not in json format.
    If you're not certain about the answer, please ask the player or say you're not sure.
    If the player has nothing in their inventory, just let the player know.
    When asked general questions that may have nothing to do with Factorio, You answer the player regardless.
    Never mention the word "assistant".
    """

def get_tools():
    return [
        LlamaCppFunctionTool(get_player_inventory),
        # LlamaCppFunctionTool(get_item_recipe),
        LlamaCppFunctionTool(calculate_max_items),
        LlamaCppFunctionTool(find_closest_item_name),
        LlamaCppFunctionTool(theoretical_requirements),
        # LlamaCppFunctionTool(get_all_item_names),
        # LlamaCppFunctionTool(get_all_items),
        # LlamaCppFunctionTool(get_technologies),
        # LlamaCppFunctionTool(get_technology_info),
        # LlamaCppFunctionTool(get_all_technologies),
        # LlamaCppFunctionTool(name="add_todo_item", description="Add a task to the player's to-do list.", function_tool=add_todo_item),
        # LlamaCppFunctionTool(name="get_todo_list", description="Get the player's to-do list.", function_tool=get_todo_list),
        # LlamaCppFunctionTool(name="update_todo_status", description="Update the status of a task on the to-do list.", function_tool=update_todo_status)
    ]


# Callback for receiving messages for the user.
# def send_message_to_user_callback(message: str):
    # print("Assistant: " + message.strip())

agent = FunctionCallingAgent(
    provider, 
    system_prompt=system_prompt, 
    llama_cpp_function_tools=get_tools(),
    # send_message_to_user_callback=send_message_to_user_callback,
    # allow_parallel_function_calling=True,
    messages_formatter_type=MessagesFormatterType.LLAMA_3,
    debug_output = True,
    # debug_output = False
    )

def generate_response(query):
    print("Query:", query)
    response = agent.generate_response(query)
    try:
        actual_response = response[0]["arguments"]["content"]
        print(actual_response)
        pass
    except Exception as e:
        print("===ERROR===")
        print("Response Type:", type(response))
        print("Model Response:", response)
        print("===END ERROR Message===")
        raise e
    # print(response)

    return actual_response

# print(generate_response("How's it going?"))