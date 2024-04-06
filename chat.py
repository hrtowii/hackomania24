import os
from openai import AzureOpenAI
from dotenv import dotenv_values

class Chatter():
    def __init__(self):
        config = dotenv_values(".env")
        self.client = AzureOpenAI(
            api_key=config["AZURE_OPENAI_API_KEY"],  
            api_version="2024-02-01",
            azure_endpoint = config["AZURE_OPENAI_ENDPOINT"]
            )
        # Either use gpt-35-turbo-instruct or gpt-35-turbo
        self.deployment_name='gpt-35-turbo' 

    def send_completion_job(self, msg):
        # Send a completion call to generate an answer
        print('Sending a test completion job')
        start_phrase = 'Write a tagline for an ice cream shop. '
        response = self.client.completions.create(model=self.deployment_name, prompt=msg, max_tokens=10)
        print(response)
        print(start_phrase+response.choices[0].text)

    def send_chat(self, msg):
        print('Sending a test chat message')
        response = self.client.chat.completions.create(
            model=self.deployment_name, # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are a helpful assistant that is meant to answer any and all questions to do with setting a businesses up in Singapore."},
                {"role": "user", "content": "How do I build the best ideas for a hackathon?"},
                {"role": "assistant", "content": "Identify real problems, leverage new technologies and validate your idea."},
                {"role": "user", "content":f"{msg}"}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content