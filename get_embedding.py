import json
import pickle
import sqlite3
import os
import asyncio
import httpx
from dotenv import load_dotenv

DB_PATH = "knowledge_base.db"
DISCOURSE_JSON = "discourse_posts.json"
MARKDOWN_JSON = "metadata.json"

load_dotenv()


# AIPipe embedding function
async def get_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://aipipe.org/openai/v1/embeddings",
            headers={"Authorization": f"Bearer {os.environ['API_KEY']}"},  # Ensure you have your API key set in .env
            json={
                "model": "text-embedding-3-small",
                "input": text
            }
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]


def insert_discourse_posts():
    with open(DISCOURSE_JSON, "r", encoding="utf-8") as f:
        posts = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for post in posts:
        content = post.get("content", "").strip()
        if not content:
            continue

        try:
            embedding = asyncio.run(get_embedding(content))
            c.execute("""
                INSERT INTO discourse_chunks (
                    post_id, topic_id, topic_title, post_number, author,
                    created_at, likes, chunk_index, content, url, embedding
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                post["post_id"], post["topic_id"], post["topic_title"],
                post["post_number"], post["author"], post["created_at"],
                post.get("like_count", 0), 0, content, post["url"],
                sqlite3.Binary(pickle.dumps(embedding))
            ))
        except Exception as e:
            print(f"Skipping post_id {post['post_id']}: {e}")

    conn.commit()
    conn.close()


def insert_markdown_docs():
    with open(MARKDOWN_JSON, "r", encoding="utf-8") as f:
        docs = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for idx, doc in enumerate(docs):
        filename = doc["filename"]
        if not os.path.exists(filename):
            print(f"Skipping {filename}: file not found.")
            continue

        with open(filename, "r", encoding="utf-8") as md_file:
            content = md_file.read().strip()

        if not content:
            print(f"Skipping {filename}: content empty.")
            continue

        try:
            embedding = asyncio.run(get_embedding(content))
            c.execute("""
                INSERT INTO markdown_chunks (
                    doc_title, original_url, downloaded_at,
                    chunk_index, content, embedding
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                doc["title"], doc["original_url"], doc["downloaded_at"],
                0, content, sqlite3.Binary(pickle.dumps(embedding))
            ))
        except Exception as e:
            print(f"Skipping {filename}: {e}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    insert_discourse_posts()
    insert_markdown_docs()
    print("✅ All embeddings stored in the database.")
