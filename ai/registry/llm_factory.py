import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.chat_models import ChatOllama

class LLMFactory:
    """Factory to abstract LLM provider instantiation."""
    
    @staticmethod
    def get_llm(temperature: float = 0.0) -> BaseChatModel:
        provider = os.getenv("LLM_PROVIDER", "groq").lower()
        
        if provider == "openai":
            return ChatOpenAI(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                temperature=temperature
            )
        elif provider == "groq":
            return ChatGroq(
                model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
                temperature=temperature
            )
        # elif provider == "gemini":
        #     return ChatGoogleGenerativeAI(
        #         model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
        #         temperature=temperature
        #     )
        # elif provider == "ollama":
        #     return ChatOllama(
        #         model=os.getenv("OLLAMA_MODEL", "llama3"),
        #         temperature=temperature
        #     )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

llm_factory = LLMFactory()
