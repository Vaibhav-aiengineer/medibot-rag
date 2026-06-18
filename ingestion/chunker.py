from pathlib import Path
import re
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

# Some source PDFs render every heading at the same visual style, so
# Docling parses them as a flat list of same-level headings with no
# parent/child nesting. As a result a content chunk (e.g. a drug
# table) ends up under a generic sub-heading like "Antimicrobial
# therapy" that no longer names the condition it belongs to. We
# reconstruct that grouping by tracking the most recent "major
# section" heading and folding it into the child chunks.

# Enumerated condition/section titles: "A. ...", "C. ...", "1. ...",
# or procedure markers like "SOP 6 ...", "Section ...".
_MAJOR_SECTION_RE = re.compile(
    r"^([A-Za-z0-9]{1,4}[.)]\s|(SOP|Section|Chapter|Protocol|Part)\b)"
)

# Document-level headings that start a fresh top-level region and so
# must NOT inherit the previous condition as a parent.
_DOC_LEVEL_RE = re.compile(
    r"^(Appendix|Disclaimer|Introduction|Overview|References?|"
    r"Standard Treatment Protocols)\b"
)


def _is_major_section(heading):
    return bool(_MAJOR_SECTION_RE.match(heading))


def _is_doc_level(heading):
    return bool(_DOC_LEVEL_RE.match(heading))


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


def chunk_document(document, document_path, chunker):
    """
    Convert a parsed Docling document into chunk records.

    The stored ``text`` is the *contextualised* chunk: HybridChunker
    prepends the chunk's own heading(s). On top of that we propagate
    the running "major section" heading (see above) so a sub-section
    chunk also carries the condition / procedure it belongs to — both
    in its embedded text and in its section title.
    """

    collection = Path(document_path).parent.name

    chunks = []
    current_major = None

    for chunk in chunker.chunk(document):

        text = chunker.contextualize(chunk)

        if not text.strip():
            continue

        headings = list(chunk.meta.headings or [])
        own_heading = headings[-1] if headings else None

        # Update / reset the running parent section.
        if own_heading and _is_major_section(own_heading):
            current_major = own_heading
        elif own_heading and _is_doc_level(own_heading):
            current_major = None

        # Fold the parent section into sub-section chunks.
        parent = current_major if current_major != own_heading else None

        if parent and not text.startswith(parent):
            text = f"{parent}\n{text}"

        if parent:
            section_title = f"{parent} > {own_heading}"
            if parent not in headings:
                headings = [parent] + headings
        elif own_heading:
            section_title = own_heading
        else:
            section_title = "Untitled"

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
                    "section_title": section_title,
                    "headings": headings,
                },
            }
        )

    return chunks
