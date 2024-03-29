import tiktoken
import os
from openai import AzureOpenAI

from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version = "2023-05-15",
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  # Your Azure OpenAI resource's endpoint value.
)

system_message = {"role": "system", "content": "You are a helpful assistant."}
max_response_tokens = 250
token_limit = 4096
conversation = []
conversation.append(system_message)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    if type(messages) == list:
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    elif type(messages) == str:
        num_tokens += len(encoding.encode(messages))
    return num_tokens
while True:
    user_input = input("Q:")      
    conversation.append({"role": "user", "content": user_input})
    conv_history_tokens = num_tokens_from_messages(conversation)

    while conv_history_tokens + max_response_tokens >= token_limit:
        del conversation[1] 
        conv_history_tokens = num_tokens_from_messages(conversation)

    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"), # model = "deployment_name".
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens,
        #stream=True
    )

    print(f"""The response object is {response}""")
    print(f"""The completion tokens count returned by AOAI {response.usage.completion_tokens}""")
    print(f"""The prompt tokens count returned by AOAI {response.usage.prompt_tokens}""")
    
    print(f"""Response is: {response.choices[0].message.content}""")
    print(f"""Conversation till now is: {conversation}""")
    print(f"""Calculated token count for response (completion) is: {num_tokens_from_messages("".join(response.choices[0].message.content))}""")
    print(f"""Calculated token count for prompt is: {num_tokens_from_messages(conversation)}""")
    conversation.append({"role": "assistant", "content": response.choices[0].message.content})