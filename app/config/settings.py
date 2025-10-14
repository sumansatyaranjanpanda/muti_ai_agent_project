from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY=os.getenv("TAVILY_API_KEY")


    MODEL_NAMES = [
    "llama-3.1-8b-instant",
    "meta-llama/llama-guard-4-12b",
    "llama-3.3-70b-versatile",
    "qwen-3-32b",
    "gpt-oss-120b"
    ]

settings=Settings()

