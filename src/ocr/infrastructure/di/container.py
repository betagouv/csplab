from dependency_injector import containers, providers

from application.usecases.extract_text_usecase import ExtractTextUsecase
from infrastructure.services.tesseract_extractor import TesseractPDFExtractor


class Container(containers.DeclarativeContainer):
    pdf_extractor = providers.Singleton(TesseractPDFExtractor)

    extract_text_usecase = providers.Factory(
        ExtractTextUsecase, extractor=pdf_extractor
    )
