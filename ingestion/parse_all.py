from loaders import get_converter, get_all_pdfs

print("Creating converter...")

converter = get_converter()

print("Finding PDFs...")

pdfs = get_all_pdfs("data")

print(f"\nFound {len(pdfs)} PDFs\n")

for pdf in pdfs:

    print("=" * 60)
    print(f"Parsing: {pdf.name}")

    try:

        result = converter.convert(str(pdf))

        markdown = result.document.export_to_markdown()

        print("SUCCESS")
        print(f"Pages: {len(result.document.pages)}")
        print(f"Tables: {len(result.document.tables)}")

        print("\nPreview:")
        print(markdown[:300])

        print("\n")

    except Exception as e:

        print("FAILED")
        print(str(e))