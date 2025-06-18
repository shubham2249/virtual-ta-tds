🎓 Virtual Teaching Assistant for TDS (IIT Madras)

This project is a virtual Teaching Assistant (TA) built using FastAPI, Gemini embeddings, and SQLite. It processes Discourse posts and markdown course content to answer student queries about the Tools in Data Science (TDS) course offered by IIT Madras.

🚀 Features
💬 Accepts student questions via an API endpoint

📚 Uses Gemini's embedding model for semantic search

🔍 Retrieves the most relevant chunks from:

Discourse forum posts

Markdown lecture notes

🧠 Stores precomputed embeddings in an SQLite database

📦 Lightweight and deployable via Docker

🗂 Project Structure
graphql
Copy
Edit
virtual-ta-tds/
├── main.py                  # FastAPI application entry point
├── get_embedding.py        # Script to embed JSON data and store in SQLite
├── discourse_posts.json    # Discourse forum data
├── metadata.json           # Markdown metadata
├── Tools_in_Data_Science.md # Downloaded course material
├── knowledge_base.db       # SQLite DB with embeddings
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container setup
└── README.md               # You're here!
