# Qdrant Hackathon Backend

Backend API for a music video processing platform with AI-powered song recommendations using Qdrant vector database.

## Features

- **AI-Powered Recommendations**: Uses Qdrant vector database and sentence transformers for semantic song matching
- **File Upload & Processing**: Handle video, audio, and image file uploads
- **RESTful API**: Built with Flask-RESTX with automatic Swagger documentation
- **Vector Search**: Semantic similarity search for song recommendations
- **CORS Support**: Configured for frontend integration

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

