from openai import OpenAI
from movie_assistant.core.config import settings


class LLMClient:

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def get_client(self):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        return client


LLM = LLMClient(settings.GROQ_PROVIDER_API_KEY, settings.GROQ_PROVIER_BASE_URL)
