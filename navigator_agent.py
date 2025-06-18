from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.llms import Ollama
from playwright_actions import navigate_bunnings

search_tool = Tool(
    name="NavigateBunnings",
    func=navigate_bunnings,
    description="Use this tool to search and navigate a product on Bunnings website."
)

def run_navigation(product_name):
    llm = Ollama(model="llama3",base_url="http://ollama:11434")

    agent = initialize_agent(
        tools=[search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    try:
        return agent.run(f"Find '{product_name}' on Bunnings.com.au, add to cart, and go to checkout.")
    except Exception as e:
        return f"Failed initial attempt: {e}. Retrying...\n" + retry_navigation(product_name)

def retry_navigation(product_name):
    try:
        return navigate_bunnings(product_name, recover=True)
    except Exception as e:
        return f"Failed on retry: {str(e)}"
