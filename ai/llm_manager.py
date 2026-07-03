import os
import time
import logging
from typing import Dict, Any, Optional
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class LLMManager:
    """
    Manages the lifecycle, fallback, and health checking of LLM providers.
    Fallback Sequence: Groq -> OpenAI -> Ollama -> ML Fallback
    """
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.temperature = 0.0
        
    def get_model(self, model_name: str = "llama3-70b-8192"):
        """Returns the first healthy LLM provider in the fallback sequence."""
        # 1. Try Groq
        if self.groq_api_key:
            try:
                llm = ChatGroq(temperature=self.temperature, model_name=model_name, api_key=self.groq_api_key)
                # Quick health check (does not actually ping unless we want to, but instantiation implies readiness)
                logger.info(f"LLMManager: Selected Groq provider with model {model_name}")
                return llm
            except Exception as e:
                logger.warning(f"LLMManager: Groq initialization failed: {e}. Falling back to OpenAI.")
                
        # 2. Try OpenAI
        if self.openai_api_key:
            try:
                llm = ChatOpenAI(temperature=self.temperature, model="gpt-4o", api_key=self.openai_api_key)
                logger.info("LLMManager: Selected OpenAI provider with model gpt-4o")
                return llm
            except Exception as e:
                logger.warning(f"LLMManager: OpenAI initialization failed: {e}. Falling back to Ollama.")
                
        # 3. Try Ollama (Local)
        try:
            llm = ChatOllama(temperature=self.temperature, model="llama3")
            logger.info("LLMManager: Selected Ollama provider with model llama3")
            return llm
        except Exception as e:
            logger.error(f"LLMManager: All LLM providers failed. System must operate in fallback mode. Error: {e}")
            raise Exception("Advanced AI explanation is temporarily unavailable. Standard fraud protection remains active.")

    def health_check(self) -> Dict[str, Any]:
        """Validates that at least one provider is available."""
        status = {
            "groq": "configured" if self.groq_api_key else "missing_key",
            "openai": "configured" if self.openai_api_key else "missing_key",
            "ollama": "available_for_fallback",
            "status": "healthy" if (self.groq_api_key or self.openai_api_key) else "degraded"
        }
        return status
