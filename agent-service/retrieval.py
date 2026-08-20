import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from langchain_postgres import PGVector

load_dotenv()

CONNECTION_STRING = "postgresql+psycopg2://postgres:postgres@localhost:5432/support_agent"
COLLECTION_NAME = "kb_docs"

embeddings = NVIDIAEmbeddings(
    model="nvidia/nv-embedqa-e5-v5",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

vectorstore = PGVector(
    embeddings=embeddings,
    collection_name=COLLECTION_NAME,
    connection=CONNECTION_STRING,
)


def search_knowledge_base(query: str, k: int = 3):
    """
    Searches the KB for the top-k most relevant chunks to the query.
    Returns a list of dicts with content, team, and similarity score.
    """
    results = vectorstore.similarity_search_with_score(query, k=k)

    formatted = []
    for doc, score in results:
        formatted.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source"),
            "section": doc.metadata.get("section"),
            "team": doc.metadata.get("team"),
            "score": score,
        })
    return formatted


if __name__ == "__main__":
    # quick manual test
    query = "my router has a red blinking light"
    results = search_knowledge_base(query)
    for r in results:
        print(f"[{r['score']:.4f}] {r['source']} / {r['section']} (team: {r['team']})")
        print(r['content'][:150])
        print()