from loaders import get_converter
from chunker import process_table

converter = get_converter()

result = converter.convert(
    "data/clinical/drug_formulary.pdf"
)

table = result.document.tables[0]

chunks = process_table(
    table,
    "data/clinical/drug_formulary.pdf"
)

print(f"Chunks Created: {len(chunks)}")

print("\nFIRST CHUNK:\n")

print(chunks[0])