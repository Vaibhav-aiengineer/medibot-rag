from pathlib import Path

from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import PdfFormatOption
from docling.datamodel.base_models import InputFormat


def get_converter():
    """
    Create Docling converter with OCR disabled.
    """

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options
            )
        }
    )

    return converter


def get_all_pdfs(data_folder="data"):
    """
    Recursively find all PDFs inside data folder.
    """

    pdf_files = list(Path(data_folder).rglob("*.pdf"))

    return pdf_files