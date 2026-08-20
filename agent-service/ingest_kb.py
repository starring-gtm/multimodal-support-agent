import os
import glob
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()

CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5432/support_agent"
COLLECTION_NAME = "kb_docs"

# Split on ## headers (our docs consistently use this level for sections
# like "Steps to resolve", "When to escalate", etc.)
HEADERS_TO_SPLIT_ON = [
    ("#", "doc_title"),
    ("##", "section"),
]

# Fallback splitter, only used if a single section is still too long
FALLBACK_SPLITTER = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)


def parse_frontmatter(content: str):
    """Pulls out the --- id/category/team --- block and returns (metadata, body)."""
    parts = content.split("---")
    metadata = {}
    body = content

    if len(parts) >= 3:
        frontmatter_raw = parts[1].strip()
        body = "---".join(parts[2:]).strip()
        for line in frontmatter_raw.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()

    return metadata, body


def load_and_chunk_docs(folder_path: str):
    documents = []
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)

    for filepath in glob.glob(os.path.join(folder_path, "*.md")):
        with open(filepath, "r") as f:
            content = f.read()

        frontmatter_metadata, body = parse_frontmatter(content)
        frontmatter_metadata["source"] = os.path.basename(filepath)

        # Step 1: split by markdown headers -> one chunk per section
        header_chunks = header_splitter.split_text(body)

        for chunk in header_chunks:
            # chunk.metadata now has doc_title/section from the headers;
            # merge with our frontmatter metadata (team, category, id)
            combined_metadata = {**frontmatter_metadata, **chunk.metadata}

            # Step 2: if a section is still too long, fall back to character splitting
            if len(chunk.page_content) > 800:
                sub_chunks = FALLBACK_SPLITTER.split_text(chunk.page_content)
                for sub_chunk in sub_chunks:
                    documents.append(Document(page_content=sub_chunk, metadata=combined_metadata))
            else:
                documents.append(Document(page_content=chunk.page_content, metadata=combined_metadata))

    return documents


def main():
    print("Loading and chunking KB docs (header-aware)...")
    docs = load_and_chunk_docs("kb_docs")
    print(f"Created {len(docs)} chunks from {len(glob.glob('kb_docs/*.md'))} files.")

    # quick peek so you can sanity-check chunk boundaries before embedding
    for d in docs[:3]:
        print("---")
        print("metadata:", d.metadata)
        print("content preview:", d.page_content[:120].replace("\n", " "), "...")

    print("\nInitializing NVIDIA embeddings...")
    embeddings = NVIDIAEmbeddings(
        model="nvidia/nv-embedqa-e5-v5",
        api_key=os.getenv("NVIDIA_API_KEY"),
    )

    print("Storing embeddings in pgvector...")
    vectorstore = PGVector.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        pre_delete_collection=True,  # wipes and recreates on each run - fine for dev/testing
    )

    print("Done. KB ingested into pgvector.")


if __name__ == "__main__":
    main()