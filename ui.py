from openai import AzureOpenAI
from dotenv import dotenv_values
from langchain.schema import AIMessage, HumanMessage
config = dotenv_values(".env")
import gradio as gr

    
client = AzureOpenAI(
    api_key=config["AZURE_OPENAI_API_KEY"],  
    api_version="2024-02-01",
    azure_endpoint = config["AZURE_OPENAI_ENDPOINT"]
    )

def predict(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model='gpt-35-turbo',
    messages= history_openai_format,
    temperature=1.0,
    stream=False)
    return response.choices[0].message.content


gr.ChatInterface(predict).launch()
