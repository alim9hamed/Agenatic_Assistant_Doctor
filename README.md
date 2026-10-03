# Assistant Doctor: AI-Powered Eye Disease Chatbot

A bilingual (Arabic / English) chatbot that answers questions about eye diseases using **Retrieval-Augmented Generation (RAG)**. Content from trusted medical websites is embedded into a vector database, and the most relevant passages are passed to a Groq-hosted LLM to produce a focused answer.

The chatbot runs as a Gradio app on **Hugging Face Spaces**, and this repository provides a lightweight **Flask REST API** (deployed on **Render**) that exposes it to any frontend or backend.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Y99MMJbsPhRcUXsKsKPjx0cIygz37ZAN?usp=sharing)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-yellow)](https://huggingface.co/spaces/alim9hamed/medical_chatbot)

> **Version note:** This branch (`main`) contains **v1**, the original proof of concept. A production-oriented rewrite with a layered (MVC-style) architecture, pluggable LLM / embedding / vector database providers, and MongoDB persistence is available on the [`production-v2`](https://github.com/alim9hamed/Agenatic_Assistant_Doctor/tree/production-v2) branch. See [What changed in v2](#what-changed-in-v2).

> ⚠️ **Medical disclaimer:** This project is for educational and research purposes only. It does **not** provide medical diagnoses and is not a substitute for a licensed ophthalmologist. For any eye problem, consult a doctor. In an emergency, contact your local emergency services.

This project is part of my graduation project, together with the [Eye Disease Classification](https://github.com/alim9hamed/eye-disease-classification-yolov8.git) computer-vision model.

---

## 🔗 Links

| Resource | Link |
| --- | --- |
| 🤗 Chatbot (Hugging Face Space) | <https://huggingface.co/spaces/alim9hamed/medical_chatbot> |
| 📓 Full notebook (Google Colab) | [Open in Colab](https://colab.research.google.com/drive/1Y99MMJbsPhRcUXsKsKPjx0cIygz37ZAN?usp=sharing) |
| 🌐 Live API (Render) | `https://<your-render-service>.onrender.com` |
| 🚀 v2 (production-oriented rewrite) | [`production-v2` branch](https://github.com/alim9hamed/Agenatic_Assistant_Doctor/tree/production-v2) |

## ✨ Features

- 🌍 **Automatic language detection**: replies in Arabic or English, matching the user's question (with RTL/LTR formatting).
- 📚 **Custom medical knowledge base** built from trusted sources: WebMD, Mayo Clinic, MedlinePlus, Healthline, and CDC.
- 🔎 **Semantic search** with ChromaDB and Hugging Face embeddings.
- 💬 **Chat history** included in the prompt for context-aware answers.
- 🩺 **Ophthalmologist persona** prompt: concise, medically grounded answers, with a clear fallback when no answer is available.
- 🔌 **Ready-to-use REST API** with CORS enabled, so web and mobile apps can call it directly.

## 🏗️ Architecture

```
┌────────────┐   POST /predict   ┌─────────────────────┐   gradio_client   ┌──────────────────────────┐
│  Frontend  │ ────────────────► │  Flask API (Render) │ ────────────────► │ Gradio app (HF Space)    │
│ / Backend  │ ◄──────────────── │  this repository    │ ◄──────────────── │ RAG chatbot + Groq LLM   │
└────────────┘      JSON         └─────────────────────┘                   └──────────────────────────┘
```

### Inside the chatbot (Hugging Face Space)

```
Medical websites ──► WebBaseLoader ──► Text splitter ──► Embeddings ──► ChromaDB
                                      (150 chars / 30 overlap)  (MiniLM-L6-v2)      │
                                                                                    │ top-2 similar chunks
User question ──► Language detection ───────────────────────────────────────────────┤
                                                                                    ▼
                                          Prompt (context + history + language) ──► Groq LLM ──► Answer
```

1. **Ingestion:** pages are loaded, split into chunks, embedded, and stored in ChromaDB.
2. **Retrieval:** the top 2 most similar chunks are retrieved for each question.
3. **Generation:** a prompt combining the context, chat history, and detected language is sent to the LLM through a LangChain QA chain.
4. **Response:** the answer is returned in the user's language.

This is a classic, fixed-pipeline RAG: every question follows the same steps (retrieve once, then generate). The model does not decide whether to search, rewrite the question, or choose between tools.

## 🧰 Tech Stack

| Component | Technology |
| --- | --- |
| Language | Python 3 |
| LLM | Groq: `meta-llama/llama-4-scout-17b-16e-instruct` (via `langchain_groq`) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector store | ChromaDB |
| Orchestration | LangChain |
| Language detection | `langdetect` |
| Chatbot UI | Gradio (Hugging Face Spaces) |
| API layer | Flask, Flask-CORS, `gradio_client` |
| Deployment | Render (API) + Hugging Face Spaces (chatbot) |

## 📁 Repository Structure

```
Agenatic_Assistant_Doctor/
├── app.py             # Flask API that forwards questions to the Hugging Face Space
├── requirements.txt   # Python dependencies
├── render.yaml        # Render deployment configuration
├── Procfile           # Process definition (start command)
└── README.md
```

> The full chatbot code (RAG pipeline, Gradio UI) lives in the Hugging Face Space and the Colab notebook.

## 📡 API Reference

### `POST /predict`

Send a question and receive the chatbot's answer.

**Request**

```json
{ "question": "ما هي أعراض المياه الزرقاء؟" }
```

**Success response** (`200`)

```json
{ "response": "..." }
```

**Errors**

| Status | Body | Reason |
| --- | --- | --- |
| `400` | `{"error": "Missing question"}` | The `question` field is empty or missing |
| `500` | `{"error": "<details>"}` | The Hugging Face Space is unreachable or failed |

**Example: cURL**

```bash
curl -X POST https://<your-render-service>.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"question": "What causes dry eye?"}'
```

**Example: Python**

```python
import requests

r = requests.post(
    "https://<your-render-service>.onrender.com/predict",
    json={"question": "What causes dry eye?"},
)
print(r.json()["response"])
```

**Example: JavaScript**

```javascript
const res = await fetch("https://<your-render-service>.onrender.com/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: "What causes dry eye?" }),
});
const data = await res.json();
console.log(data.response);
```

## 🚀 Getting Started

### Run the API locally

```bash
# 1. Clone
git clone https://github.com/alim9hamed/Agenatic_Assistant_Doctor.git
cd Agenatic_Assistant_Doctor

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server (default port 8000)
python app.py
```

The API will be available at `http://localhost:8000/predict`.

### Deploy on Render

1. Push this repository to GitHub.
2. In Render, create a new **Web Service** from the repository (Render reads `render.yaml`).
3. Make sure the start command runs the Flask app (for example `gunicorn app:app`).
4. Deploy, then use the generated URL as your API base.

### Run the chatbot itself

The chatbot needs a [Groq API key](https://console.groq.com/).

- **Hugging Face Space:** add `GROQ_API_KEY` under *Settings → Variables and secrets*.
- **Google Colab:** add `GROQ_API_KEY` in Colab *Secrets* and run the notebook cells in order.

> Never commit API keys or tokens to the repository.

## ⚙️ Chatbot Configuration

| Setting | Default |
| --- | --- |
| LLM model | `meta-llama/llama-4-scout-17b-16e-instruct` |
| Embedding model | `all-MiniLM-L6-v2` |
| Chunk size / overlap | 150 / 30 |
| Retrieved chunks (k) | 2 |
| Vector DB directory | `chroma_db` |
| Knowledge sources | WebMD, Mayo Clinic, MedlinePlus, Healthline, CDC |

## ⚠️ Limitations

- The knowledge base is built from the **landing pages** of the listed websites, so coverage of specific eye diseases can be limited. Adding direct links to eye-disease pages will improve answers.
- Answers depend on retrieved context and the LLM; they can be incomplete or inaccurate.
- The API depends on the Hugging Face Space being awake. On free tiers, the first request after inactivity can be slow.
- The RAG logic is not part of this repository (it lives in the Space and the notebook), and the knowledge base is fixed rather than uploaded by the user.

These limitations are the main motivation for v2.

## What changed in v2

The [`production-v2`](https://github.com/alim9hamed/Agenatic_Assistant_Doctor/tree/production-v2) branch rebuilds the system as a production-oriented backend:

| Area | v1 (this branch) | v2 |
| --- | --- | --- |
| Where the RAG logic lives | Hugging Face Space and Colab; this repo is a thin proxy | Inside the repository, as a structured application |
| Code organization | Single-file API | MVC-style layers: routes, controllers, models, stores, helpers |
| Knowledge ingestion | Fixed list of website landing pages | File upload API (`.txt`, `.pdf`) with validation |
| LLM / embeddings | One provider and one model each | Multiple providers through `LLMInterface`, `EmbeddingInterface`, and a factory |
| Vector database | ChromaDB | Pluggable backend selected through configuration |
| Persistent storage | Vector store only | MongoDB (projects, files, chunks) plus the vector database |
| Chunking and retrieval | Fixed (150 / 30, top-2) | Configurable per request |
| Multiple knowledge bases | No | Project-based isolation |

v2 is an early version and is still under active development. See its README for the full comparison, architecture diagrams, and setup instructions.

## 🤝 Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add your feature"`
4. Push and open a Pull Request

## 📄 License

This project is licensed under the [Apache License 2.0](https://github.com/alim9hamed/Agenatic_Assistant_Doctor/blob/main/LICENSE). See the `LICENSE` file for details.

---

⭐ If you find this project useful, please give it a star!
