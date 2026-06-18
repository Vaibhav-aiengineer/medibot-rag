from pathlib import Path

from docling.document_converter import DocumentConverter
from docling.document_converter import PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat
from docling.backend.pypdfium2_backend import (
    PyPdfiumDocumentBackend
)


# Document formats we ingest. Markdown is parsed by Docling too,
# so the same converter handles both PDFs and .md files.
SUPPORTED_SUFFIXES = {".pdf", ".md"}


def get_converter():
    """
    Create a Docling converter for PDF + Markdown.

    OCR is disabled (our source PDFs are digital text) and page
    rasterisation is turned off. The pypdfium2 backend is used
    because the default backend rasterises every page at high DPI,
    which exhausts memory (std::bad_alloc) on the larger documents.
    """

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.generate_page_images = False
    pipeline_options.generate_picture_images = False

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                backend=PyPdfiumDocumentBackend,
            )
        }
    )

    return converter


def get_all_documents(data_folder="data"):
    """
    Recursively find all supported documents (PDF + Markdown)
    inside the data folder.
    """

    files = [
        path
        for path in Path(data_folder).rglob("*")
        if path.suffix.lower() in SUPPORTED_SUFFIXES
    ]

    return sorted(files)
