from domain.interfaces.pdf_extractor import IPDFTextExtractor


class ExtractTextUsecase:
    def __init__(self, extractor: IPDFTextExtractor):
        self.extractor = extractor

    async def execute(self, pdf_content: bytes) -> str:
        return await self.extractor.extract_text(pdf_content)
