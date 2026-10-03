from abc import ABC, abstractmethod

class EmbeddingInterface(ABC):

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        pass