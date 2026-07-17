# Corporate AI Agent - E-commerce Context

An AI-powered corporate agent designed to help employees access internal knowledge across multiple document formats using RAG (Retrieval-Augmented Generation).

## 🛠️ Tech Stack
- **LLM**: Google Gemini 1.5 Flash
- **Framework**: LangChain
- **Vector Store**: FAISS
- **Frontend**: Streamlit
- **Infrastructure**: OCI Compute (Oracle Linux) + Podman (Docker compatible)

## 🚀 Deployment Guide (Oracle Cloud Infrastructure)

### 1. Prerequisites
- An OCI Compute Instance running Oracle Linux.
- An API Key from Google AI Studio.

### 2. Prepare the Instance
Connect to your instance via SSH:
```bash
ssh -i /path/to/your/key opc@<YOUR_PUBLIC_IP>
```

Install necessary tools:
```bash
sudo dnf install -y git podman
# Alias docker to podman
alias docker=podman
```

### 3. Setup the Project
```bash
git clone https://github.com/jairvides/challenge-alura-agent.git
cd challenge-alura-agent
```

### 4. Environment Configuration
Create a `.env` file and add your Google API key:
```bash
nano .env
# Paste: GOOGLE_API_KEY=your_key_here
# Save: Ctrl+O, Enter, Ctrl+X
```

### 5. Build and Run
**Importante**: Asegúrate de tener la carpeta `vectorstore/` generada (corriendo `python ingest.py` localmente) antes de construir la imagen.

Build the container image:
```bash
docker build -t corporate-ai-agent .
```

Run the container:
```bash
docker run -d -p 8501:8501 --env-file .env corporate-ai-agent
```

### 6. Verify
Access your agent via your browser at `http://<YOUR_PUBLIC_IP>:8501`.

### 7. Deploy
![image alt](https://github.com/jairvides/challenge-alura-agent/blob/cd3bc7e1dea0b710dcd7abd164e8d591bf6c62ae/img/deploy1.png)
![image alt](https://github.com/jairvides/challenge-alura-agent/blob/5cd0aba0aba0acbae0cda9e911e443c5a7452c0c/img/deploy2.png)
![image alt](https://github.com/jairvides/challenge-alura-agent/blob/5cd0aba0aba0acbae0cda9e911e443c5a7452c0c/img/deploy3.png)
![image alt](https://github.com/jairvides/challenge-alura-agent/blob/5cd0aba0aba0acbae0cda9e911e443c5a7452c0c/img/deploy4.png)

---

## 🧪 Troubleshooting
If you encounter `ModuleNotFoundError` during ingestion, ensure all dependencies are installed:
```bash
python -m pip install -r requirements.txt
```
If you get `docker: command not found`, use `podman` instead or ensure `podman-docker` is installed.
