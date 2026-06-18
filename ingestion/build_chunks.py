import json
import sys

from docling.datamodel.base_models import ConversionStatus

from loaders import get_converter, get_all_documents
from chunker import get_chunker, chunk_document


def main():

    converter = get_converter()
    chunker = get_chunker()

    documents = get_all_documents("data")

    print(f"Found {len(documents)} documents")

    all_chunks = []
    failures = []

    for path in documents:

        print(f"\nProcessing: {path.name}")

        result = converter.convert(str(path))

        # Guard: Docling can return SUCCESS with pages silently
        # dropped (e.g. on a backend memory error). Refuse to build
        # an index from a partial parse instead of failing quietly.
        if result.status not in (
            ConversionStatus.SUCCESS,
            ConversionStatus.PARTIAL_SUCCESS,
        ):
            print(f"  PARSE FAILED: {result.status}")
            failures.append((path.name, str(result.status)))
            continue

        if result.status == ConversionStatus.PARTIAL_SUCCESS:
            print(f"  WARNING: partial parse for {path.name}")
            failures.append((path.name, "PARTIAL_SUCCESS"))

        chunks = chunk_document(
            result.document,
            str(path),
            chunker,
        )

        print(f"  {len(chunks)} chunks")

        all_chunks.extend(chunks)

    print(f"\nTotal chunks created: {len(all_chunks)}")

    if failures:
        print("\nDocuments with parse problems:")
        for name, status in failures:
            print(f"  - {name}: {status}")

    # Don't overwrite a good index with a broken one.
    if not all_chunks:
        print("\nNo chunks produced; aborting without writing.")
        sys.exit(1)

    with open(
        "data/chunks.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("\nSaved to data/chunks.json")


if __name__ == "__main__":
    main()
