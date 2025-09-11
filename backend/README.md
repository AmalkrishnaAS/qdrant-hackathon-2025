# Backend API

Flask-based backend API for the Qdrant Hackathon music video processing platform.

> **Note**: For complete project setup and overview, see the [main README](../README.md) in the project root.

## Quick Start

### Prerequisites
- Python 3.8+
- Docker and Docker Compose (for running Qdrant and Redis)
- Bun package manager (for frontend development)

### Local Development Setup

1. **Clone the repository** (if you haven't already)
   ```bash
   git clone https://github.com/your-username/qdrant-hackathon-2025.git
   cd qdrant-hackathon-2025/backend
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your configuration (see [Configuration](#configuration) section below).

3. **Start the required services** (Qdrant and Redis)
   ```bash
   docker-compose up -d
   ```

4. **Set up a virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Initialize the database**
   ```bash
   python run.py init-db
   ```

6. **Run the development server**
   ```bash
   python app.py
   ```
   Or run with hot reload:
   ```bash
   flask run --debug
   ```

7. **Run Celery worker** (in a separate terminal)
   ```bash
   celery -A celery_worker.celery worker --loglevel=info
   ```

8. **Access the API documentation**
   Visit [http://localhost:5000/docs/](http://localhost:5000/docs/) for interactive API documentation.

## Configuration

Copy `.env.example` to `.env` and update the following variables as needed:

- `SECRET_KEY`: A secret key for Flask session management
- `QDRANT_*`: Configure your Qdrant connection
- `UPSTASH_REDIS_*`: Required for Redis caching
- `CELERY_*`: Configure Celery broker and result backend
- `CORS_ORIGINS`: Comma-separated list of allowed origins

For development, you can use the default values in `.env.example` with the following services running:
- Qdrant: `localhost:6333` (started via Docker Compose)
- Redis: `localhost:6379` (started via Docker Compose)

## Core Features

- **AI-Powered Recommendations**: Semantic song matching with Qdrant vector database
- **File Processing**: Video, audio, and image upload handling
- **RESTful API**: Flask-RESTX with automatic Swagger documentation
- **Vector Search**: Real-time similarity search for recommendations

## API Endpoints

### Songs
- `GET /api/songs/trending` - Get trending songs
- `GET /api/songs/` - List all songs with optional category filter
- `POST /api/songs/recommendations` - Get AI-powered song recommendations
- `GET /api/songs/{id}/download` - Download processed files

### Upload & Processing
- `POST /api/upload/` - Upload files (video, audio, images)
- `POST /api/upload/process` - Process uploaded video with selected audio
- `GET /api/upload/status/{processing_id}` - Check processing status

### Health
- `GET /api/health/` - API and service health check

## Setup Instructions

### Prerequisites

- Python 3.8+
- Qdrant vector database running (Docker recommended)
- Bun package manager

### 1. Start Qdrant Database

```bash
# Using Docker (recommended)
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 2. Install Dependencies

```bash
# Using bun for package management
bun install

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Make sure QDRANT_HOST and QDRANT_PORT match your Qdrant instance
```

### 4. Initialize Database

```bash
# Initialize Qdrant with seed data
bun run init-qdrant
```

### 5. Start Development Server

```bash
# Start Flask development server
bun run dev

# Or directly with Python
python app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

Once the server is running, visit `http://localhost:5000/docs/` for interactive Swagger documentation.

## Configuration

Key configuration options in `.env`:

- `QDRANT_HOST`: Qdrant server host (default: localhost)
- `QDRANT_PORT`: Qdrant server port (default: 6333)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 100MB)

## Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── api/                  # API endpoints
│   │   ├── songs.py         # Song-related endpoints
│   │   ├── upload.py        # File upload endpoints
│   │   └── health.py        # Health check endpoint
│   ├── models/
│   │   └── schemas.py       # Pydantic data models
│   └── services/
│       ├── qdrant_service.py # Qdrant integration
│       └── data_service.py   # Data management
├── config/
│   └── config.py            # Configuration classes
├── uploads/                 # Uploaded files directory
├── static/processed/        # Processed files directory
├── requirements.txt         # Python dependencies
├── package.json            # Bun package configuration
├── .env.example           # Environment variables template
└── app.py                # Application entry point
```

## Development

### Running Tests

```bash
bun run test
```

### Code Linting

```bash
bun run lint
```

### Production Deployment

```bash
# Install production dependencies
pip install gunicorn

# Start production server
bun run start
```

## Vector Database Integration

The application uses Qdrant for:

1. **Song Embeddings**: Each song's metadata is converted to vector embeddings using sentence transformers
2. **Similarity Search**: Find similar songs based on text queries or uploaded content
3. **Recommendations**: AI-powered recommendations using vector similarity

## File Processing

Currently supports:
- **Video**: MP4, AVI, MOV, MKV, WebM
- **Audio**: MP3, WAV, FLAC, AAC, M4A
- **Images**: JPG, JPEG, PNG, GIF, BMP, WebP

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License

