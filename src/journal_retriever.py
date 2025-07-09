from typing import List, Dict


def retrieve_journal(collection, journal_id: str) -> Dict:
    """function to get all chunks for the particular journal_id"""
    results = collection.get(
        limit=1000,   # this should be large enough to get all chunks
        where={"source_doc_id":journal_id},
        include=["metadatas", "documents"]
    )

    # metadatas and document
    metadatas = results["metadatas"]
    documents = results["documents"]

    # check if there are no documents
    if not metadatas:
        raise ValueError(f"No chunks found for journal '{journal_id}")
    
    # Extract shared metadata from the first hit
    first = metadatas[0]
    common = {
        "journal_id": journal_id,
        "publish_year": first["publish_year"],
        "link": first["link"] 
    }
    
    # ordered chunk list
    chunks = []
    for meta, doc in sorted(zip(metadatas, documents), key=lambda x:x[0]["chunk_index"]):
        chunks.append({
            "id": meta["id"],
            "chunk_index": meta["chunk_index"],
            "section_heading": meta["section_heading"],
            "attributes": meta["attributes"],
            "text": doc
        })
        
    return {**common, "chunks": chunks}


if __name__=="__main__":
    from chunking import get_chroma_collection
    
    journal_id = "extension_brief_mucuna.pdf"
    collection = get_chroma_collection()
    retrieved_data = retrieve_journal(collection=collection, journal_id=journal_id)
    print(retrieved_data)
    
    