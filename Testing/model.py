import os
from llama_cpp import Llama
from llama_cpp_agent import LlamaCppFunctionTool, FunctionCallingAgent, MessagesFormatterType
from llama_cpp_agent.providers import LlamaCppPythonProvider
from llama_cpp_agent.chat_history import BasicChatHistory, BasicChatMessageStore, BasicChatHistoryStrategy

from api import get_inventory, get_recipe, get_all_items, get_technologies, get_technology_info, get_all_technologies
# from todo import add_todo_item, get_todo_list, update_todo_status
# from retriever import Retriever
# import torch

# Load pre-trained model

# model_path = os.getenv("USERPROFILE") + "/.cache/huggingface/hub/models--QuantFactory--Meta-Llama-3-8B-Instruct-GGUF-v2/snapshots/94f17b2f2d72645fce9555f0395954a34db24e1e/Meta-Llama-3-8B-Instruct-v2.Q8_0.gguf"
model_path = os.getenv("USERPROFILE") + r"\.cache\lm-studio\models\lmstudio-community\Meta-Llama-3.1-8B-Instruct-GGUF\Meta-Llama-3.1-8B-Instruct-Q4_K_M-take2.gguf"

print(model_path)
# use_gpu = torch.cuda.is_available()

llm = Llama(
    model_path=model_path, 
    n_gpu_layers=-1,
    chat_format="llama-3",
    verbose=True,
    n_ctx=8192
)

# Set up the provider
provider = LlamaCppPythonProvider(llm)

# Create a message store for the chat history
# chat_history_store = BasicChatMessageStore()

# Create the actual chat history, by passing the wished chat history strategy, it can be last_k_message or last_k_tokens. The default strategy will be to use the 20 last messages for the chat history.
# We will use the last_k_tokens strategy which will include the last k tokens into the chat history. When we use this strategy, we will have to pass the provider to the class.
# chat_history = BasicChatHistory(message_store=chat_history_store, chat_history_strategy=BasicChatHistoryStrategy.last_k_tokens, k=7000, llm_provider=provider)

# Example documents (In a real scenario, these could be game guides, FAQs, etc.)
# documents = [
#     "Factorio is a game in which you build and manage factories.",
#     "You can get iron plates by smelting iron ore in a furnace.",
#     "Research allows you to unlock new technologies and upgrades.",
#     "Use transport belts to move items around your factory.",
#     "Power your machines with steam engines or solar panels."
# ]

# retriever = Retriever(documents)

# System prompt to guide the model's responses
system_prompt = """
    You are a smart and helpful gaming assistant for the game Factorio. 
    You provide accurate and concise information, about the game or anything else.
    You can retrieve player inventory, get item recipes, list all items in the game.
    Help the player to the best of your abilities.
    If the player asks for how much of an item they can make, check the recipe for the item and compare that to the items they have in their inventory.
    Sometimes, some recipes may require intermediate products to make, and the player may have the items to make them, based on what they have in their inventory, let them know the total of the item they can make.
    If the player doesn't have enough to make the item, explain to the player what else do they need and how much.
    If you're not certain about the answer, please ask or say you're not sure.
    """
# context = f"System: {system_prompt}\n"
conversation_history = []
# <|start_header_id|>system<|end_header_id|>You are a helpful AI assistant.<|eot_id|>
# <|start_header_id|>user<|end_header_id|>Hi!<|eot_id|>
# <|start_header_id|>assistant<|end_header_id|>Hello there! It's great to meet you!<|eot_id|>

# def generate_context(system_prompt, conversation):
#     # context = f"System: {system_prompt}\n"
#     for turn in conversation:
#         role = "User" if turn["role"] == "user" else "Assistant" if turn["role"] == "assistant" else "API"
#         context += f"{role}: {turn['content']}\n"
#     return context


# def interpret_user_input(user_input):
#     # Determine if the input requires an API call and what kind
#     if "inventory" in user_input.lower():
#         return "inventory"
#     elif "recipe" in user_input.lower():
#         return "recipe"
#     elif "technologies" in user_input.lower():
#         return "technologies"
#     elif "technology info" in user_input.lower():
#         return "technology_info"
#     elif "all technologies" in user_input.lower():
#         return "all_technologies"
#     elif "add to-do" in user_input.lower():
#         return "add_todo"
#     elif "show to-do" in user_input.lower():
#         return "show_todo"
#     elif "mark to-do" in user_input.lower():
#         return "mark_todo"
#     return None

# def make_api_call(api_type, user_input):
#     if api_type == "inventory":
#         return get_inventory()
#     elif api_type == "recipe":
#         item_name = user_input.split("recipe of")[-1].strip()
#         return get_recipe(item_name)
#     elif api_type == "technologies":
#         return get_technologies()
#     elif api_type == "technology_info":
#         tech_name = user_input.split("technology info of")[-1].strip()
#         return get_technology_info(tech_name)
#     elif api_type == "all_technologies":
#         return get_all_technologies()
#     elif api_type == "add_todo":
#         task = user_input.split("add to-do")[-1].strip()
#         add_todo_item(task)
#         return f"Task '{task}' added to your to-do list."
#     elif api_type == "show_todo":
#         todos = get_todo_list()
#         return "\n".join([f"{todo[0]}: {todo[1]} [{todo[2]}]" for todo in todos])
#     elif api_type == "mark_todo":
#         parts = user_input.split("mark to-do")[-1].strip().split(" ")
#         task_id = int(parts[0])
#         status = parts[-1]
#         update_todo_status(task_id, status)
#         return f"Task {task_id} marked as {status}."
#     return None

# def generate_response(query):
#     # Add the new user input to the conversation
#     conversation_history.append({"role": "user", "content": query})

#     # Interpret user input to determine if an API call is needed
#     api_type = interpret_user_input(query)
#     if api_type:
#         # Make the API call
#         api_response = make_api_call(api_type, query)
#         # Add API response to the conversation
#         conversation_history.append({"role": "api", "content": str(api_response)})

#     # Generate the context from the updated conversation
#     context = generate_context(system_prompt, conversation_history)

#     # Generate response using the model
#     response = llm(context, max_tokens=150)["choices"][0]["text"].strip()

#     # Add the model's response to the conversation
#     conversation_history.append({"role": "assistant", "content": response})
#     print("convo history: ", conversation_history)
#     return response

def get_tools():
    return [
        LlamaCppFunctionTool(get_inventory),
        LlamaCppFunctionTool(get_recipe),
        LlamaCppFunctionTool(get_all_items),
        # LlamaCppFunctionTool(get_technologies),
        # LlamaCppFunctionTool(get_technology_info),
        # LlamaCppFunctionTool(get_all_technologies),
        # LlamaCppFunctionTool(name="add_todo_item", description="Add a task to the player's to-do list.", function_tool=add_todo_item),
        # LlamaCppFunctionTool(name="get_todo_list", description="Get the player's to-do list.", function_tool=get_todo_list),
        # LlamaCppFunctionTool(name="update_todo_status", description="Update the status of a task on the to-do list.", function_tool=update_todo_status)
    ]


# Callback for receiving messages for the user.
def send_message_to_user_callback(message: str):
    print("Assistant: " + message.strip())

agent = FunctionCallingAgent(
    provider, 
    system_prompt=system_prompt, 
    llama_cpp_function_tools=get_tools(),
    # chat_history=chat_history, 
    # send_message_to_user_callback=send_message_to_user_callback,
    # allow_parallel_function_calling=True,
    messages_formatter_type=MessagesFormatterType.LLAMA_3,
    debug_output = True
    )
def generate_response(query):
    # conversation_history.append({"role": "user", "content": query})

    # Create function calling agent
    # provider = LlamaCppPythonProvider(
    #     llm, 
    #                          system_prompt=system_prompt, 
    #                          messages=conversation_history, 
    #                          max_tokens=150,
    #                          stop=["<|eot_id|>"],
    #                          temperature=0.5)
    response = agent.generate_response(query)
    
    # Add the model's response to the conversation
    # conversation_history.append({"role": "assistant", "content": response})

    return response