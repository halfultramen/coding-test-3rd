# backend/app/services/embeddings.py
from app.core.config import settings

try:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
except TypeError:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
    client = None  # fallback mode

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY not configured in .env")

    print(f"[DEBUG] Generating embeddings for {len(texts)} text(s)...")

    try:
        if client:
            print("[DEBUG] Using new OpenAI client...")
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            print("[DEBUG] Response received from OpenAI API.")
            embeddings = [item.embedding for item in response.data]
        else:
            print("[DEBUG] Using legacy OpenAI API...")
            response = openai.Embedding.create(
                model="text-embedding-3-small",
                input=texts
            )
            print("[DEBUG] Response received from legacy API.")
            embeddings = [d["embedding"] for d in response["data"]]

        print(f"[DEBUG] Generated {len(embeddings)} embeddings successfully.")
        return embeddings

    except Exception as e:
        import traceback
        print(f"[ERROR] Failed to generate embeddings: {e}")
        traceback.print_exc()
        return []
