from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_SUBSCRIPTION"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name = os.getenv("AZURE_SEARCH_INDEX"),
    credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
)

def embed(text: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input = text
    )
    return response.data[0].embedding
    

def vecotirize_existing_docs(batch_size=100):
    print(f"Starting vector synchronization for index: {search_client._index_name}...")
    results = search_client.search(
        search_text="*",
        select=["id", "content"],
        include_total_count=True
    )
    total_docs = results.get_count()
    print(f"Found {total_docs} documents in the index.")
    upload_batch = []
    docs_to_update_count = 0

    for doc in results:
        doc_id = doc["id"]
        content = doc["content"]
        if "contentVector" in doc and doc["contentVector"]:
            continue

        try:
            vector = embed(content)
            upload_doc = {
                "id": doc_id,
                "contentVector": vector
            }
            upload_batch.append(upload_doc)
            docs_to_update_count += 1
        except Exception as e:
            print(f"ERROR processing document {doc_id}: {e}")
            continue

        if len(upload_batch) >= batch_size:
            print(f"Uploading batch of {len(upload_batch)} documents...")
            search_client.merge_or_upload_documents(upload_batch)
            upload_batch = []
        
    if upload_batch:
        print(f"Uploading final batch of {len(upload_batch)} documents...")
        search_client.merge_or_upload_documents(upload_batch)

if __name__ == "__main__":
    # Ensure your deployment name is set in .env
    vecotirize_existing_docs()
