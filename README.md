# Setup and Dependencies

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- [uv](https://github.com/astral-sh/uv) - Python package installer and resolver (install via `curl -sSf https://astral.sh/uv/install.sh | sh`)
- Mistral AI API key (set as `MISTRAL_API_KEY` environment variable)
- YouTube Music API credentials (optional)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd qdrant-hack
   ```

2. **Set up Python environment**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
    ```

3. **Configure environment variables**
   ```bash
   # Set your Mistral API key
   export MISTRAL_API_KEY=your_mistral_api_key
   # Optional: export YTMUSIC_COOKIE=your_ytmusic_cookie
   

4. **Start Qdrant database**
   ```bash
   docker-compose up -d
   ```
   This will start Qdrant on port 6333.

## Dependencies

Managed by `uv` and `pyproject.toml`:
- crewai
- langchain
- mistralai
- qdrant-client
- ytmusicapi
