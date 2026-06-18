from pathlib import Path
import uuid

from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import (
    HuggingFaceTokenizer,
)
from docling_core.types.doc.labels import DocItemLabel
from transformers import AutoTokenizer


# Role-based access control by source folder (collection).
ROLE_MAPPING = {
    "clinical": ["doctor", "admin"],
    "billing": ["billing_executive", "admin"],
    "nursing": ["nurse", "doctor", "admin"],
    "equipment": ["technician", "admin"],
    "general": ["all"],
}

# Embedding model whose tokenizer drives the token-aware size limit.
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
MAX_TOKENS = 512


def get_chunker():
    """
    Build a Docling HybridChunker.

    HybridChunker first splits along the document's natural
    structure (section -> subsection -> paragraph / table), then
    applies a token-aware second pass: oversized elements are split
    and undersized peers under the same heading are merged, all
    bounded by the embedding model's token limit.
    """

    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(EMBEDDING_MODEL),
        max_tokens=MAX_TOKENS,
    )

    return HybridChunker(
        tokenizer=tokenizer,
        merge_peers=True,
    )


def _chunk_type(chunk):
    """
    Classify a chunk by the doc items it contains so structured
    content (tables, code) can be told apart from prose.
    """

    labels = {item.label for item in chunk.meta.doc_items}

    if DocItemLabel.TABLE in labels:
        return "table"

    if DocItemLabel.CODE in labels:
        return "code"

    return "section"


def _section_title(chunk):
    """
    Most specific parent heading for the chunk, falling back to the
    document title when no sub-heading is present.
    """

    headings = chunk.meta.headings or []

    if headings:
        return headings[-1]

    return "Untitled"


def chunk_document(document, document_path, chunker):
    """
    Convert a parsed Docling document into chunk records.

    The stored ``text`` is the *contextualised* chunk: HybridChunker
    prepends the parent section heading(s), so each chunk's embedded
    text carries its structural context.
    """

    collection = Path(document_path).parent.name

    chunks = []

    for chunk in chunker.chunk(document):

        text = chunker.contextualize(chunk)

        if not text.strip():
            continue

        headings = chunk.meta.headings or []

        chunks.append(
            {
                "id": str(uuid.uuid4()),
                "text": text,
                "metadata": {
                    "document": Path(document_path).name,
                    "collection": collection,
                    "access_roles": ROLE_MAPPING.get(
                        collection,
                        ["admin"],
                    ),
                    "chunk_type": _chunk_type(chunk),
                    "section_title": _section_title(chunk),
                    "headings": headings,
                },
            }
        )

    return chunks
