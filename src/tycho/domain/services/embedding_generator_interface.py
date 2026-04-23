from typing import List, Protocol


class IEmbeddingGenerator(Protocol):
    async def generate_embedding(self, text: str) -> List[float]: ...
