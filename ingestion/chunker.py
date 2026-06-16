from pathlib import Path
import uuid


ROLE_MAPPING = {
    "clinical": ["doctor", "admin"],
    "billing": ["billing", "admin"],
    "nursing": ["nurse", "doctor", "admin"],
    "equipment": ["technician", "admin"],
    "general": ["all"]
}


def create_table_chunk(headers, row):

    lines = []

    for header, cell in zip(headers, row):

        lines.append(
            f"{header}: {cell.text}"
        )

    return "\n".join(lines)


def create_chunk(text, document_path):

    collection = Path(document_path).parent.name

    return {
    "id": str(uuid.uuid4()),

    "text": text,

    "metadata": {

        "document": Path(document_path).name,

        "collection": collection,

        "access_roles": ROLE_MAPPING.get(
            collection,
            ["admin"]
        ),

        "chunk_type": "table_row"
    }
}

def process_table(table, document_path):

    chunks = []

    headers = [
        cell.text
        for cell in table.data.grid[0]
    ]

    for row in table.data.grid[1:]:

        chunk_text = create_table_chunk(
            headers,
            row
        )

        chunk = create_chunk(
            chunk_text,
            document_path
        )

        chunks.append(chunk)

    return chunks

def process_section_document(markdown, document_path):

    chunks = []

    sections = markdown.split("\n## ")

    for section in sections:

        section = section.strip()

        if not section:
            continue

        lines = section.split("\n")

        heading = lines[0].replace("#", "").strip()

        content = "\n".join(lines[1:]).strip()

        if not content:
            continue

        text = f"Section: {heading}\n\n{content}"

        chunk = create_chunk(
            text,
            document_path
        )

        chunk["metadata"]["chunk_type"] = "section"

        chunks.append(chunk)

    return chunks