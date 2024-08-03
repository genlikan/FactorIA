import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from api import get_inventory, get_recipe, get_technologies, get_technology_info, get_all_technologies
from todo import add_todo_item, get_todo_list, update_todo_status
from retriever import Retriever

# Load pre-trained model and tokenizer
model_id = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF-v2"
filename = "Meta-Llama-3-8B-Instruct-v2.Q8_0.gguf"

tokenizer = AutoTokenizer.from_pretrained(model_id, gguf_file=filename, use_fast=False)
model = AutoModelForCausalLM.from_pretrained(model_id, gguf_file=filename)

# Set eos_token as the pad_token
tokenizer.pad_token = tokenizer.eos_token

# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

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
system_prompt = (
    "You are a helpful assistant for the game Factorio. You provide accurate and concise information about the game. "
    "You can retrieve player inventory, get item recipes, list technologies, and provide details about technologies. "
    "You can also manage to-do lists for the player."
)

def generate_response(query):
    # Retrieve relevant documents
    # retrieved_docs = retriever.retrieve(query)
    
    # Combine system prompt, retrieved documents, and user query
    # context = system_prompt + " ".join(retrieved_docs) + " " + query
    context = system_prompt + " " + query
    
    # Check if the query is about the inventory
    if "inventory" in query.lower():
        inventory = get_inventory()
        context += " " + str(inventory)
    
    # Tokenize and encode the input context
    inputs = tokenizer(context, return_tensors="pt", padding=True, truncation=True).to(device)
    
    # Generate response using the model
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=150,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Append specific information based on query type
    if "recipe" in query.lower():
        item_name = query.split("recipe of")[-1].strip()
        recipe = get_recipe(item_name)
        response += f"\nRecipe for {item_name}: {recipe}"
    elif "technologies" in query.lower():
        technologies = get_technologies()
        response += f"\nCurrent Technologies: {technologies}"
    elif "technology info" in query.lower():
        tech_name = query.split("technology info of")[-1].strip()
        tech_info = get_technology_info(tech_name)
        response += f"\nTechnology Info for {tech_name}: {tech_info}"
    elif "all technologies" in query.lower():
        all_techs = get_all_technologies()
        response += f"\nAll Technologies: {all_techs}"
    elif "add to-do" in query.lower():
        task = query.split("add to-do")[-1].strip()
        add_todo_item(task)
        response += f"\nTask '{task}' added to your to-do list."
    elif "show to-do" in query.lower():
        todos = get_todo_list()
        todo_list = "\n".join([f"{todo[0]}: {todo[1]} [{todo[2]}]" for todo in todos])
        response += f"\nYour to-do list:\n{todo_list}"
    elif "mark to-do" in query.lower():
        task_id = int(query.split("mark to-do")[-1].strip().split(" ")[0])
        status = query.split("mark to-do")[-1].strip().split(" ")[-1]
        update_todo_status(task_id, status)
        response += f"\nTask {task_id} marked as {status}."

    return response
