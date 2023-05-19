from flask import request
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import Cohere
from langchain.agents import initialize_agent
from langchain.tools import DuckDuckGoSearchRun

app = Flask(__name__)

def initialize_agent_chain():
    search = DuckDuckGoSearchRun()
    tools = [
        Tool(
            name="Search",
            func=search.run,
            description="useful for when you need to answer questions about current events"
        )
    ]

    llm = Cohere(cohere_api_key='IDFTOw7ZUP6SPnpPs4qwt633ooSSI7mgmF33lcKW')

    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
    return agent_chain

@app.route('/', methods=['POST'])
def process_input():
    input_string = request.form['input']
    agent_chain = initialize_agent_chain()
    result = agent_chain.run(input_string)
    return result

if __name__ == '__main__':
    app.run()
