from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from langchain_core.messages import SystemMessage, HumanMessage
from app.config.settings import settings

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt):
    llm = ChatGroq(model=llm_id)
    
    # Create tools without topic parameter
    tools = [TavilySearch(max_results=2)] if allow_search else []
    
    # Create agent
    agent = create_react_agent(model=llm, tools=tools)
    
    # Prepare messages with system prompt at the beginning
    messages = []
    if system_prompt and system_prompt.strip():
        messages.append(SystemMessage(content=system_prompt))
    
    # Add user queries as HumanMessage
    for q in query:
        if isinstance(q, str):
            messages.append(HumanMessage(content=q))
        else:
            messages.append(q)
    
    state = {"messages": messages}
    response = agent.invoke(state)
    response_messages = response.get("messages", [])
    
    # Extract only AI messages and filter out tool calls
    ai_messages = []
    for message in response_messages:
        if isinstance(message, AIMessage):
            # Check if the message has actual content (not just tool calls)
            if message.content and not message.content.startswith("<function="):
                ai_messages.append(message.content)
    
    # Return the last meaningful AI response
    if ai_messages:
        return ai_messages[-1]
    else:
        # If no clean AI message, try to get any AI message content
        for message in reversed(response_messages):
            if isinstance(message, AIMessage) and message.content:
                return message.content
        return "No response generated"