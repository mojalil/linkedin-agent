from langgraph.graph import Graph, END
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, LLMNode
from .state import FlowState
from . import logger

def create_graph() -> Graph:
    """Create and configure the LangGraph workflow."""
    # Initialize the planner model
    planner_model = ChatOpenAI(
        model="gpt-4",
        temperature=0.7
    )
    
    # Create the planner node
    planner = LLMNode(planner_model)
    
    # Initialize the graph
    g = Graph()
    
    # Add the planner node
    g.add_node("plan", planner)
    
    # Set the entry point
    g.set_entry_point("plan")
    
    # Set the finish point
    g.set_finish_point(END)
    
    logger.info("Created LangGraph workflow")
    return g

# Create a global graph instance
graph = create_graph()
