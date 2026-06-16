import json

from loaders import get_converter, get_all_pdfs
from chunker import (
    process_table,
    process_section_document
)

TABLE_HEAVY_DOCS = {
    "billing_codes.pdf",
    "diagnostic_reference.pdf",
    "drug_formulary.pdf",
    "treatment_protocols.pdf"
}


converter = get_converter()

all_chunks = []

pdfs = get_all_pdfs("data")

print(f"Found {len(pdfs)} PDFs")


for pdf in pdfs:

    print(f"\nProcessing: {pdf.name}")

    result = converter.convert(str(pdf))

    # Table documents
    if pdf.name in TABLE_HEAVY_DOCS:

        print("Using Table Chunker")

        for table in result.document.tables:

            chunks = process_table(
                table,
                str(pdf)
            )

            all_chunks.extend(chunks)

    # Everything else for now
    else:

        print("Using Section Chunker")

        markdown = result.document.export_to_markdown()

        chunks = process_section_document(
            markdown,
            str(pdf)
        )

        all_chunks.extend(chunks)


print(f"\nTotal Chunks Created: {len(all_chunks)}")


with open(
    "data/chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print("\nSaved to data/chunks.json")