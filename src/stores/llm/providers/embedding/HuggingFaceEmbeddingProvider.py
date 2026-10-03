from ...interfaces import EmbeddingInterface
from huggingface_hub import InferenceClient
import logging


class HuggingFaceEmbeddingProvider(EmbeddingInterface):

    def __init__(self, api_key: str, model_id: str):
        self.api_key = api_key
        self.model_id = model_id
        self.embedding_size = None

        self.client = InferenceClient(
            api_key=self.api_key
        )

        self.logger = logging.getLogger(__name__)

    def set_embedding_model(self, model_id: str, embedding_size: int):

        self.model_id = model_id
        self.embedding_size = embedding_size
        
    def embed_text(self, text: str, document_type: str = None):

        if not self.client:
            self.logger.error("HuggingFace client was not set")
            return None

        embedding = self.client.feature_extraction(
            text,
            model=self.model_id
        )

        return embedding.tolist()