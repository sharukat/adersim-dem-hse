# Disaster & Emergency Management and Health, Safety & Environment (HSE) Insights AI-Assistant
This is an AI-driven platform that retrieves, analyzes, and surfaces accurate information from YouTube videos related to Disaster & Emergency Management (DEM) and Health, Safety & Environment (HSE). It semantically evaluates video content using Large Language Models (LLMs) to answer user queries using Retrieval Augmented Generation (RAG) with context-rich responses while displaying the relevant videos within the application.

## 🌱 Motivation
In fields like DEM and HSE, timely and accurate access to information can be critical. However, valuable insights are often locked inside unstructured video content. This project was created to address the gap by:
- Automatically identifying and retrieving relevant videos from YouTube.
- Extracting and semantically validating their transcripts for alignment with user queries.
- Chunking the transcripts intelligently and storing them in a vector database for fast, accurate retrieval.
- Providing an integrated conversational AI assistant to surface insights interactively and visually.


## 🚀 Getting Started
### Frontend
1. **Navigate to the frontend directory and install dependencies using the provided package-lock.toml.**
   ```bash
   cd frontend
   npm install
   ```
2. **Build and run the development server.**
   ```bash
   npm run build
   npm start
   ```
### Backend
1. **Ensure Docker and Docker Compose are installed.**
2. **Run the backend services using Docker Compose.**
   ```bash
   docker-compose up --build
   ```
   This will start:
   - The backend service (Flask)
   - MongoDB (for storing metadata and sentiment/topic analysis)
   - Qdrant (for vector storage of chunked transcripts)
   - Ollama (for embeddings and LLM responses)
3. **Before running the backend, ensure:**
   - The Ollama container has the Nomic embedding model downloaded.
   - A Groq API Key is available for chat model inference.
  
## 💻 Technology Stack
<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=python,typescript,fastapi,nextjs,tailwindcss,docker,langchain,ollama,groq,youtube"
    />
  </a>
</p>

## 📹 Demo
![dem_hse_trimmed-latest](https://github.com/user-attachments/assets/8111149f-dd40-423a-9f78-e538eeda493b)
