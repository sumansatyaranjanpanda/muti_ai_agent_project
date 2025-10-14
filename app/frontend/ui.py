import streamlit as st
import requests
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi AI Agent", layout='centered')
st.title("Multi AI Agent")

system_prompt = st.text_area(
    "Define Your AI Agent Behaviour (Ex: Healthcare agent, Financial agent, etc):",
    height=70
)
selected_model = st.selectbox("Select your AI model:", settings.MODEL_NAMES)
allow_web_search = st.checkbox("Allow web search")
query = st.text_area("Enter your query:", height=150)

api_url = "http://127.0.0.1:8000/chat"

if st.button("Ask Agent") and query.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "query": [query],
        "allow_search": allow_web_search,
    }
    
    try:
        logger.info("Sending request to backend")
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            agent_response = response.json().get("response", "")
            logger.info("Successfully received response from backend")
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.error(f"Backend error: {response.status_code}")
            error_detail = response.json().get("detail", "Unknown error")
            st.error(f"Error in backend: {error_detail}")
            
    except requests.exceptions.Timeout:
        logger.error("Request timeout")
        st.error("Request timed out. Please try again.")
        
    except Exception as e:
        logger.error(f"Something error in backend: {str(e)}")
        st.error(f"Failed to communicate with Backend: {str(e)}")