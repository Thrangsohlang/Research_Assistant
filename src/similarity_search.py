from typing import List, Dict
from src.utils.logger_RA import logger 

def semantic_search(
    collection,
    query_embedding: List[float],
    k: int,
    min_score: float
) -> List[Dict]:
    logger.log_info(
        f"[semantic_search] Starting search: k={k}, min_score={min_score}"
    )
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            include=["distances", "metadatas", "documents"]
        )
        logger.log_info(
            f"[semantic_search] Retrieved {len(results['ids'][0])} raw results"
        )
    except Exception as e:
        logger.log_error(f"[semantic_search] Query failed: {e}")
        raise

    hits: List[Dict] = []
    for idx, score in zip(results["ids"][0], results["distances"][0]):
        if score > min_score:
            logger.log_info(
                f"[semantic_search] Skipping id='{idx}' with score={score}"
            )
            continue
        i = results["ids"][0].index(idx)
        hit = {
            "id": idx,
            "score": score,
            "metadata": results["metadatas"][0][i],
            "document": results["documents"][0][i]
        }
        logger.log_info(f"[semantic_search] Accepting hit: {hit['id']} (score={score})")
        hits.append(hit)

    logger.log_info(f"[semantic_search] Completed search with {len(hits)} hits")
    return hits


if __name__ == "__main__":
    from chunking import get_chroma_collection, embed_texts

    test_query = "why grow the velvet bean?"
    logger.log_info(f"[semantic_search][main] Embedding test query: '{test_query}'")
    query_emb = embed_texts(test_query)

    collection = get_chroma_collection()
    logger.log_info(f"[semantic_search][main] Running semantic_search on collection '{collection.name}'")
    hits = semantic_search(collection, query_emb, 10, 0.25)

    logger.log_info(f"[semantic_search][main] Results:\n{hits}")
    print(hits)
