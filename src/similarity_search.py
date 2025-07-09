from typing import List, Dict

def semantic_search(collection, query_embedding: List[float], k: int, min_score: float) -> List[Dict]:
    # results
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["distances", "metadatas", "documents"]
    )

    # filter out the results
    hits = []
    
    for idx, score in zip(results["ids"][0], results["distances"][0]):
        if score > min_score:
            continue  # skip if less
        i = results["ids"][0].index(idx)
        hits.append({
            "id": idx,
            "score": score,
            "metadata": results["metadatas"][0][i],
            "document": results["documents"][0][i]
        })
        
    return hits


if __name__=="__main__":
    from chunking import get_chroma_collection, embed_texts
    query = " why grow the velvet bean?"
    query_emb = embed_texts(query)
    collection = get_chroma_collection()
    hits = semantic_search(collection, query_emb, 10, 0.25)
    print(hits)