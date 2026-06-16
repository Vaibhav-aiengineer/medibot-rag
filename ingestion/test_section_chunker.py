from loaders import get_converter
from chunker import process_section_document

converter = get_converter()

result = converter.convert(
    "data/general/staff_handbook.pdf"
)

markdown = result.document.export_to_markdown()

chunks = process_section_document(
    markdown,
    "data/general/staff_handbook.pdf"
)

print(f"Chunks Created: {len(chunks)}")

print("\nFIRST CHUNK:\n")

print(chunks[0])