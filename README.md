## 🧠 Agentic Multigent Assignment - AI Agent Crew

An intelligent agent-based system that processes user queries with optional document context using [CrewAI](https://github.com/joaomdmoura/crewAI) and OpenAI models. This solution supports both a FastAPI backend and a user-friendly Streamlit frontend.

---

### 🔧 Tech Stack

* **CrewAI** – Multi-agent orchestration
* **OpenAI** – LLMs for reasoning and content generation
* **FastAPI** – Backend API server
* **Streamlit** – Optional frontend UI
* **Python** – Core language
* **pypdf**– For extracting text from uploaded PDFs

---

### 📁 Directory Structure

```
Agentic_Multigent_assignment/
│
├── app.py                  # 🚀 FastAPI backend with /process-query
├── streamlit_app.py        # 🎯 Streamlit UI (optional)
├── agents_config.py        # 🧠 Agent definitions
├── agent_task.py           # 📌 Task logic (includes manager delegation)
├── requirements.txt        # 📦 Project dependencies
├── .env                    # 🔐 API keys
└── README.md               # 📖 You're here!
```

---

### 🚀 How to Run

#### 1. 🔨 Installation

```bash
git clone <your-repo-url>
cd Agentic_Multigent_assignment

conda create -n crewdemo python=3.12 # for Mac
conda activate crewdemo

pip install -r requirements.txt
```

#### 2. 🔐 Setup `.env`

Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serperapi_key
```

#### 3. 🧪 Run Backend API

```bash
uvicorn app:app --reload
```

Then visit: [http://localhost:8000/docs](http://localhost:8000/docs) to test the `/process-query` API using Swagger UI.

#### 4. 🖼️ Run Frontend (Optional)

```bash
streamlit run streamlit_app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

### 🧠 Features

✅ Supports intelligent query routing with 3 agents:

* **Document Specialist**: summarizes uploaded files
* **Query Responder**: answers from documents
* **Research Agent**: fetches real-time internet info if no doc or partial info

✅ Auto-detects and parses:

* `.pdf` via `pypdf`
* `.docx` via `python-docx`
* `.txt` as plain text

✅ Works even without file upload — fetches info from the internet using Research Agent.

---Here's a complete and clean `README.md` tailored for your **CrewAI Multimodal Agent Assignment** with FastAPI backend, optional file upload (PDF only in current version), and document-query understanding:

---

# 🚀 AI Agent Crew API

An intelligent multi-agent system powered by **CrewAI** and **OpenAI**, allowing users to:

* Upload a **document (PDF)**
* Ask a **natural language question**
* Receive answers using document analysis, web research, or LLM-based querying

---

## 📦 Project Structure

```bash
.
├── app.py                    # FastAPI backend with document + query handling
├── agents_config.py          # Contains all agent definitions
├── agent_task.py             # Contains task routing logic for CrewAI
├── .env                      # API keys and config
├── requirements.txt          # All Python dependencies
└── README.md                 # You're here!
```

---

## 🛠️ Technologies Used

* `FastAPI` — RESTful API Framework
* `CrewAI` — Multi-agent orchestration library
* `OpenAI` — LLM backbone
* `PyPDF2` — For extracting text from uploaded PDFs
* `dotenv` — For secure environment variable loading
* `Uvicorn` — ASGI server for FastAPI

---

## 🔧 Setup Instructions

### 1. Clone the repo & create virtual environment

```bash
git clone <your-repo-url>
cd Agentic_Multigent_assignment

conda create -n crewdemo python=3.12
conda activate crewdemo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your environment variables in `.env`

```env
OPENAI_API_KEY=your-openai-api-key
```

---

## 🚀 Run the Application

```bash
uvicorn app:app --reload
```

Now visit: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
You’ll see the Swagger UI to test the `/process-query` API.

---

## 📤 API Usage

### Endpoint: `/process-query`

**Method**: `POST`
**Form fields**:

| Field | Type         | Required | Description                       |
| ----- | ------------ | -------- | --------------------------------- |
| query | string       | ✅        | User's natural language query     |
| file  | Upload (PDF) | optional | Optional PDF document for context |

---

## ✅ Example Use Cases

* Ask: `"What is the interest rate mentioned?"` → Upload a loan offer PDF
* Ask: `"When is capital of India?"` → No file uploaded → It fetches live info using `Research Agent`

---

## 🔄 Agent Workflow

* **Manager Agent** decides whether to:

  * Use **Document Agent** for summarization & keywords
  * Use **Query Agent** to answer using provided doc
  * Use **Research Agent** for real-time internet search

* Uses **Hierarchical Process** flow in CrewAI

---

## 🔒 Supported File Formats (Currently)

* ✅ `.pdf`

📌 *Planned support for `.docx`, `.txt`, `.md`, etc. coming soon.*

---

