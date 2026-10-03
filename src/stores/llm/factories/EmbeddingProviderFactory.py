from ..enums import EmbeddingEnums
from ..providers.llm import OpenAIProvider, CoHereProvider, OllamaProvider
from ..providers.embedding import HuggingFaceEmbeddingProvider


class EmbeddingProviderFactory:

    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):

        if provider == EmbeddingEnums.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                api_url=self.config.OPENAI_API_URL,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS
            )

        if provider == EmbeddingEnums.COHERE.value:
            return CoHereProvider(
                api_key=self.config.COHERE_API_KEY,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS
            )

        if provider == EmbeddingEnums.HUGGINGFACE.value:
            return HuggingFaceEmbeddingProvider(
                api_key=self.config.HUGGINGFACE_API_KEY,
                model_id=self.config.EMBEDDING_MODEL_ID
            )

        if provider == EmbeddingEnums.OLLAMA.value:
            return OllamaProvider(
                api_key=self.config.OLLAMA_API_KEY,
                api_url=self.config.OLLAMA_API_URL,
                default_input_max_characters=self.config.INPUT_DAFAULT_MAX_CHARACTERS
            )

        return None

