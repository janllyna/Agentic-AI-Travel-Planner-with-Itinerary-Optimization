from langchain_community.chat_models import ChatOllama
from langchain.agents.react.agent import create_react_agent
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate

from tools.flight_tool import search_flights
from tools.hotel_tool import recommend_hotel
from tools.places_tool import discover_places
from tools.budget_tool import estimate_budget

llm = ChatOllama(
    model="llama3",
    temperature=0
)

tools = [
    search_flights,
    recommend_hotel,
    discover_places,
]


REACT_PROMPT = PromptTemplate.from_template(
    """You are a travel planning agent.

You have access to the following tools:
{tools}

Tool names: {tool_names}

Use the following format:

Thought: reason about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat as needed)
Final Answer: the completed travel plan

Begin!

Question: {input}

{agent_scratchpad}"""
)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=REACT_PROMPT
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)
