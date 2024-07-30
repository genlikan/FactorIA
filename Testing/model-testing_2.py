from llama_cpp import Llama
from api import get_inventory, get_recipe, get_technologies, get_technology_info, get_all_technologies
from todo import add_todo_item, get_todo_list, update_todo_status
from retriever import Retriever
import torch

# Load pre-trained model
model_path = "Meta-Llama-3-8B-Instruct-v2.Q8_0.gguf"
use_gpu = torch.cuda.is_available()

llm = Llama(
    model_path=model_path, 
    n_gpu_layers=-1,
    chat_format="llama-3",
    verbose=False,
    n_ctx=2048
)

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
    You are a helpful AI assistant.
    You are a helpful assistant for the game Factorio. You provide accurate and concise information about the game.
    You can retrieve player inventory, get item recipes, list technologies, and provide details about technologies.
    You can also manage to-do lists for the player.
    """
context = f"System: {system_prompt}\n"
conversation_history = []
# <|start_header_id|>system<|end_header_id|>You are a helpful AI assistant.<|eot_id|>
# <|start_header_id|>user<|end_header_id|>Hi!<|eot_id|>
# <|start_header_id|>assistant<|end_header_id|>Hello there! It's great to meet you!<|eot_id|>

def generate_context(system_prompt, conversation):
    context = f"System: {system_prompt}\n"
    for turn in conversation:
        role = "User" if turn["role"] == "user" else "Assistant" if turn["role"] == "assistant" else "API"
        context += f"{role}: {turn['content']}\n"
    return context


def interpret_user_input(user_input):
    # Determine if the input requires an API call and what kind
    if "inventory" in user_input.lower():
        return "inventory"
    elif "recipe" in user_input.lower():
        return "recipe"
    elif "technologies" in user_input.lower():
        return "technologies"
    elif "technology info" in user_input.lower():
        return "technology_info"
    elif "all technologies" in user_input.lower():
        return "all_technologies"
    elif "add to-do" in user_input.lower():
        return "add_todo"
    elif "show to-do" in user_input.lower():
        return "show_todo"
    elif "mark to-do" in user_input.lower():
        return "mark_todo"
    return None

def make_api_call(api_type, user_input):
    if api_type == "inventory":
        return get_inventory()
    elif api_type == "recipe":
        item_name = user_input.split("recipe of")[-1].strip()
        return get_recipe(item_name)
    elif api_type == "technologies":
        return get_technologies()
    elif api_type == "technology_info":
        tech_name = user_input.split("technology info of")[-1].strip()
        return get_technology_info(tech_name)
    elif api_type == "all_technologies":
        return get_all_technologies()
    elif api_type == "add_todo":
        task = user_input.split("add to-do")[-1].strip()
        add_todo_item(task)
        return f"Task '{task}' added to your to-do list."
    elif api_type == "show_todo":
        todos = get_todo_list()
        return "\n".join([f"{todo[0]}: {todo[1]} [{todo[2]}]" for todo in todos])
    elif api_type == "mark_todo":
        parts = user_input.split("mark to-do")[-1].strip().split(" ")
        task_id = int(parts[0])
        status = parts[-1]
        update_todo_status(task_id, status)
        return f"Task {task_id} marked as {status}."
    return None

def generate_response(query):
    # Add the new user input to the conversation
    conversation_history.append({"role": "user", "content": query})

    # Interpret user input to determine if an API call is needed
    api_type = interpret_user_input(query)
    if api_type:
        # Make the API call
        api_response = make_api_call(api_type, query)
        # Add API response to the conversation
        conversation_history.append({"role": "api", "content": str(api_response)})

    # Generate the context from the updated conversation
    context = generate_context(system_prompt, conversation_history)

    # Generate response using the model
    response = llm(context, max_tokens=150)["choices"][0]["text"].strip()

    # Add the model's response to the conversation
    conversation_history.append({"role": "assistant", "content": response})
    print("convo history: ", conversation_history)
    return response

