from openai import AzureOpenAI
from dotenv import dotenv_values
from langchain.schema import AIMessage, HumanMessage
config = dotenv_values(".env")
import gradio as gr
from main import RAG

    
class UI:
    def __init__(self):
        self.rag = RAG()
        self.history = []
    

    def predict(self, message, history):
        history_openai_format = []
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})

        # Add rag context and display
        prompt = self.rag.compose_prompt(message)
        history_openai_format.append({"role": "user", "content": prompt})
        response = self.rag.chatter.client.chat.completions.create(
            model=self.rag.chatter.deployment_name, 
            messages=history_openai_format
        )
        return f"Qn: {prompt}\n\n" + response.choices[0].message.content

    def launch(self):
        gr.ChatInterface(
            fn=self.predict,
            title="RAG Chatbot",
            description="A chatbot that can answer questions about setting up a business in Singapore.",
            examples=[
                ["How do I start a business in Singapore?"],
                ["What is the best way to build a business?"],
            ],
        ).launch()

if __name__ == "__main__":
    ui = UI()
    ui.launch()