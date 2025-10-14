from app.core.ai_agent import get_response_from_ai_agent

print(get_response_from_ai_agent(
    llm_id="llama-3.1-8b-instant",
    query=["what is hypertension"],
    allow_serach=True,
    system_prompt="You are a healthcare assistant"
))