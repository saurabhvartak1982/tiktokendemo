# Tiktoken demo
There are scenarios where the **Prompt tokens** and the **Completion tokens** are required to be calculated in an Azure OpenAI related projects.

There are two ways in which the response can be received from an Azure OpenAI deployment in a calling program as below:
- Streaming disabled (stream=False)
- Streaming enabled (stream=True)

When streaming is **not enabled**, then Azure OpenAI returns the count of **Prompt tokens** and **Completion tokens**. 
However, when streaming is **enabled** these counts are not returned by Azure OpenAI - in case of which the tokens need to be calculated by the calling program. 

The included source code files present the logic for calculating the Azure OpenAI tokens in the scenarios of **streaming enabled** and **streaming disabled**.

## Using the source code files
The source code builds on top of a sample mentioned in the document - https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt?tabs=python-new&pivots=programming-language-chat-completions#managing-conversations 

There are 2 code files as below:
- **tiktokendemo_nonstream.py**: An example of fetching token count returned by Azure OpenAI as well as counting tokens when streaming is **disabled**. Below snippet of the code where streaming is disabled.
```
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"), # model = "deployment_name".
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens,
        #stream=True
    )
```

- **tiktokendemo_stream.py**: An example of counting Azure OpenAI tokens when streaming is **enabled**. Below snippet of the code where streaming is enabled.
```
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHATGPT_DEPLOYMENT"), # model = "deployment_name".
        messages=conversation,
        temperature=0.7,
        max_tokens=max_response_tokens,
        stream=True
    )
```

Below are the steps to be carried out to use the code:
- **Step 1**: Install dependencies
```pip install -r requirements.txt```

- **Step 2**: Rename **sampleenv** to **.env**

- **Step 3**: Fill up the details in the **.env** file

- **Step 4**: To use **tiktokendemo_nonstream.py**
Run this program as below:
```python tiktokendemo_nonstream.py```

On running the above program, you will be prompted to enter a question. Basis the response to the question, you will receive the number of tokens returned by Azure OpenAI and also the calculated tokens as marked in the below image:

![Output of tiktokendemo_nonstream.py](/images/tiktokendemo_nonstream.png)

- **Step 5**: To use **tiktokendemo_stream.py**
Run this program as below:
```python tiktokendemo_stream.py```

On running the above program, you will be prompted to enter a question. Basis the response to the question, you will receive the number of tokens calculated as marked in the below image:

![Output of tiktokendemo_stream.py](/images/tiktokendemo_stream.png)

## Thank you and acknowledgements
Satish Dadha (https://github.com/sdadha)
Laziz Turakulov (https://github.com/LazaUK)
