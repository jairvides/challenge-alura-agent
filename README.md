# Corporate AI Agent - E-commerce Context

An AI-powered corporate agent designed to help employees access internal knowledge across multiple document formats using RAG (Retrieval-Augmented Generation).

## 🚀 Features
- **Multi-format Support**: Processes PDF, Word, Excel, CSV, JSON, HTML, and Markdown.
- **RAG Pipeline**: Uses Gemini 1.5 Flash and FAISS for accurate, context-aware retrieval.
- **Interactive UI**: Streamlit-based chat interface for ease of use.
- **Cloud Ready**: Dockerized for easy deployment on Oracle Cloud Infrastructure (OCI).

## 🛠️ Tech Stack
- **LLM**: Google Gemini 1.5 Flash
- **Framework**: LangChain
- **Vector Store**: FAISS
- **Frontend**: Streamlit
- **Infrastructure**: OCI Compute + Docker

## 📦 Local Setup

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/your-username/challenge-alura-agent.git
cd challenge-alura-agent
\`\`\`

### 2. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure Environment
Create a \`.env\` file based on \`.env.example\`:
\`\`\`bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
\`\`\`

### 4. Ingest Documents
Place your corporate documents in the \`data/\` folder and run:
\`\`\`bash
python ingest.py
\`\`\`

### 5. Run the App
\`\`\`bash
streamlit run src/app.py
\`\`\`

## ☁️ OCI Deployment

### Deployment Steps:
1. **Create OCI Compute Instance**: Launch a VM instance (e.g., Ampere A1 or AMD).
2. **Install Docker**:
   \`\`\`bash
   sudo yum install -y docker
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker $USER
   \`\`\`
3. **Configure Security List**: Open ingress port `8501` in the OCI VCN Security List.
4. **Deploy**:
   \`\`\`bash
   docker build -t corporate-ai-agent .
   docker run -d -p 8501:8501 --env-file .env corporate-ai-agent
   \`\`\`

## 📺 Demo
![Agent Demo](https://via.placeholder.com/800x400?text=Agent+Running+on+OCI+Cloud)
*(Replace this with your actual image/video link)*

## 🧪 Testing
\`\`\`bash
pytest tests/
\`\`\`
