# Import the necessary classes for the pydantic tool and the agent
from enum import Enum
from typing import Union

from pydantic import BaseModel, Field

from llama_cpp_agent import FunctionCallingAgent
from llama_cpp_agent import MessagesFormatterType
from llama_cpp_agent import LlamaCppFunctionTool
from llama_cpp_agent.providers import LlamaCppPythonProvider

from llama_cpp import Llama

model_path = "Meta-Llama-3-8B-Instruct-v2.Q8_0.gguf"

llm = Llama(
    model_path=model_path, 
    n_gpu_layers=-1,
    chat_format="llama-3",
    verbose=False,
    n_ctx=2048
)

# Set up the provider
provider = LlamaCppPythonProvider(llm)


# Simple calculator tool for the agent that can add, subtract, multiply, and divide.
class MathOperation(Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class Calculator(BaseModel):
    """
    Perform a math operation on two numbers.
    """

    number_one: Union[int, float] = Field(
        ...,
        description="First number.")
    number_two: Union[int, float] = Field(
        ...,
        description="Second number.")
    operation: MathOperation = Field(..., description="Math operation to perform.")

    def run(self):
        print("I'M RUNNING")
        if self.operation == MathOperation.ADD:
            return self.number_one + self.number_two
        elif self.operation == MathOperation.SUBTRACT:
            return self.number_one - self.number_two
        elif self.operation == MathOperation.MULTIPLY:
            return self.number_one * self.number_two
        elif self.operation == MathOperation.DIVIDE:
            return self.number_one / self.number_two
        else:
            raise ValueError("Unknown operation.")


# Callback for receiving messages for the user.
def send_message_to_user_callback(message: str):
    print(message)


# Create a list of function call tools.
function_tools = [LlamaCppFunctionTool(Calculator)]

# Create the function calling agent. We are passing the provider, the tool list, send message to user callback and the chat message formatter. Also, we allow parallel function calling.
function_call_agent = FunctionCallingAgent(
    provider,
    llama_cpp_function_tools=function_tools,
    allow_parallel_function_calling=True,
    send_message_to_user_callback=send_message_to_user_callback,
    messages_formatter_type=MessagesFormatterType.LLAMA_3)

# Define the user input.
user_input = "What is 3+2?"
function_call_agent.generate_response(user_input)