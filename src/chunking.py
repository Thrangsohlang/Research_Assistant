# Splitting the text into chunks, Embed it using embedding model, Add metadata, write to vector database
import json
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer


# get the embedding models
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# initialize chromadb
client = chromadb.PersistentClient(
    path="./chroma_db"
)

def get_chroma_collection():
    # Create collection name
    collection = client.get_or_create_collection("journals")
    return collection


def read_document(filepath:str):
    # read the document
    # extract the text by pages
    # saved as list
    # return the list of extracted text
    return
    
def split_text_into_chunks(texts: List): 
    # read the list of extracted texts
    # for each page, chunk them accordingly by paragraph
    # check if paragraph exceeds the token limits
    # if so then proceed to split them further
    # append the chunk index
    # return the dict of chunks with chunk_index, section name  and paragraph index
    return
    
def create_metadata(texts: Dict):
    # read the dict
    # create id with contentName_chunkIndex_sectionName_paragraphIndex
    # feed the text to llm to get the attributes
    # populate link, texts, usage_count, source_doc_id, chunk_index, journal, publish year, section heading
    # return dict of metadata
    return

def embedding_texts(text:str):
    """function to embed the texts"""
    # embed the text
    emb = embed_model.encode(text).tolist()  # embeddings in a list
    
    return emb


def prepare_upsert_payload(
    chunks: List[Dict]
) -> Tuple[List[str], List[List[float]], List[Dict], List[str]]:
    """
    Extracts ids, embeddings, metadata, and documents from a list of chunks
    so they’re ready to upsert into ChromaDB.
    """
    ids: List[str] = []
    embs: List[List[float]] = []
    metadatas: List[Dict] = []
    documents: List[str] = []
    
    for chunk in chunks:
        text = chunk["text"]
        _id = chunk["id"]
        meta = {k: v for k, v in chunk.items() if k != "text" or "attributes"}
        meta["attributes"] = ", ".join(chunk["attributes"])  # join the attributes by comma
        emb = embedding_texts(text)
        
        ids.append(_id)
        embs.append(emb)
        metadatas.append(meta)
        documents.append(text)
    
    return ids, embs, metadatas, documents


def upsert(collection, ids: List[str], embs: List[List[float]], metadatas: List[Dict], documents: List[str]) -> str:
    """
    Upsert a batch of document chunks into a ChromaDB collection, persisting them to disk.

    This function takes pre-computed embedding vectors and associated metadata for a set of
    document chunks and writes them into the specified ChromaDB collection. After upserting,
    it persists the database to ensure durability.

    Parameters
    ----------
    collection : chromadb.api.Collection
        The ChromaDB collection instance into which the records will be upserted.
    ids : List[str]
        Unique identifiers for each document chunk.
    embs : List[List[float]]
        Embedding vectors corresponding to each document chunk.
    metadatas : List[Dict]
        A list of metadata dictionaries for each document chunk (excluding the raw text).
    documents : List[str]
        The raw text content of each document chunk to store alongside metadata.

    Returns
    -------
    str
        A success message confirming that the upsert operation completed.

    Raises
    ------
    Exception
        Propagates any exception encountered during the upsert or persist operations.
    """
    try:
        # Upsert embeddings, metadata, and raw text into the collection
        collection.upsert(
            ids=ids,
            embeddings=embs,
            metadatas=metadatas,
            documents=documents
        )
    
        return "Successfully upserted documents to ChromaDB!"
    except Exception as e:
        # Log error and re-raise for upstream handling
        print(f"Error while upserting: {e}")
        raise
        
    
    
    
    
    
    

if __name__ == "__main__":
    with open(r"Files\Sample_chunks.json", "r", encoding="utf-8") as f:
        docs = json.load(f)
    
    collection = get_chroma_collection()
    
    ids, embs, metadatas, documents = prepare_upsert_payload(docs)
    
    print(upsert(collection, ids, embs, metadatas, documents))
    