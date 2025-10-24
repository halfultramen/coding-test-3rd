# backend/app/services/query_engine.py

import os
import json
from openai import OpenAI
from app.services.embeddings import generate_embeddings
from app.services.vector_store import VectorStore
from app.db.session import SessionLocal
from app.services.metrics_calculator import get_metrics_breakdown

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handle_query(query: str, fund_id: int | None = None):
    """
    Retrieve relevant chunks, compute metrics, and generate contextual LLM response.
    Also sync latest metrics into vector store.
    """
    query_emb = generate_embeddings([query])[0]

    vs = VectorStore(index_name=f"fund_{fund_id or 'global'}")

    if fund_id:
        db = SessionLocal()
        try:
            metrics_data = get_metrics_breakdown(fund_id)
            metrics_text = json.dumps(metrics_data["metrics"], indent=2)
            metrics_emb = generate_embeddings([metrics_text])[0]
            vs.add_texts(
                [f"Updated Metrics for Fund {fund_id}:\n{metrics_text}"],
                [metrics_emb]
            )
        except Exception as e:
            print(f"[WARN] Failed to update vector store with latest metrics: {e}")
        finally:
            db.close()
    
    results = vs.search(query_emb, top_k=3) or []

    db = SessionLocal()
    try:
        metrics = get_metrics_breakdown(fund_id) if fund_id else None
    except Exception as e:
        print(f"[ERROR] Failed to get metrics for fund {fund_id}: {e}")
        metrics = None
    finally:
        db.close()

    # Siapkan context
    context = "\n".join([r["text"] for r in results]) or "No relevant context found."

    metrics_text = ""
    if metrics:
        metrics_text = (
            f"DPI: {metrics.get('metrics', {}).get('DPI', 'N/A')}\n"
            f"PIC: {metrics.get('metrics', {}).get('PIC', 'N/A')}\n"
            f"IRR: {metrics.get('metrics', {}).get('IRR', 'N/A')}\n"
        )

    system_prompt = f"""
You are a professional fund performance analyst assistant.
You can analyze and explain private equity fund performance metrics (PIC, IRR, DPI)
based on provided data and database context. 
If available, use numeric values accurately from metrics and retrieved text.

Fund Metrics:
{metrics_text}

Context from uploaded documents:
{context}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.3,
    )

    answer = completion.choices[0].message.content.strip()

    return {
        "answer": answer,
        "metrics": metrics,
        "sources": [r["text"] for r in results],
    }
