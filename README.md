# Qdrant Hackathon 2025 - Music Video Platform

A full-stack music video processing platform with AI-powered song recommendations using Qdrant vector database. This platform allows users to upload videos, get intelligent song suggestions, and create enhanced video content with synchronized audio.

## 🚀 Features

- **AI-Powered Music Recommendations**: Semantic song matching using Qdrant vector database and sentence transformers
- **Video Processing**: Upload and process video files with audio replacement
- **Interactive Frontend**: Modern React/Next.js interface with beautiful animations
- **RESTful API**: Flask-based backend with automatic Swagger documentation
- **Vector Search**: Advanced similarity search for personalized recommendations
- **Real-time Processing**: File upload with processing status tracking

## 🏗️ Architecture

This project is organized as a monorepo with separate frontend and backend services:

```
qdrant-hackathon-2025/
├── frontend/          # Next.js + React frontend
├── backend/           # Flask API backend
├── .gitignore        # Git ignore rules for both projects
└── README.md         # This file
```

## 🛠️ Quick Start

### Prerequisites

- **Backend**: Python 3.8+, Docker (for Qdrant)
- **Frontend**: Node.js 18.17+, npm/yarn/pnpm/bun
- **Database**: Qdrant vector database

### 1. Start Qdrant Database

```bash
# Run Qdrant using Docker
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 2. Setup Backend

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start the Flask development server
python app.py

# Backend will be available at http://localhost:5000
```

### 3. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
bun install
# or npm install / yarn install / pnpm install

# Start the development server
bun dev
# or npm run dev / yarn dev / pnpm dev

# Frontend will be available at http://localhost:3000
```

## 📚 Backend API Documentation

### Core Endpoints

#### Songs & Recommendations
- `GET /api/songs/trending` - Get trending songs
- `GET /api/songs/` - List all songs with optional category filter
- `POST /api/songs/recommendations` - Get AI-powered song recommendations
- `GET /api/songs/{id}/download` - Download processed files

#### File Upload & Processing
- `POST /api/upload/` - Upload files (video, audio, images)
- `POST /api/upload/process` - Process uploaded video with selected audio
- `GET /api/upload/status/{processing_id}` - Check processing status

#### Health & Monitoring
- `GET /api/health/` - API and service health check

### Interactive API Documentation

Once the backend is running, visit `http://localhost:5000/docs/` for interactive Swagger documentation.

### Supported File Formats

- **Video**: MP4, AVI, MOV, MKV, WebM
- **Audio**: MP3, WAV, FLAC, AAC, M4A
- **Images**: JPG, JPEG, PNG, GIF, BMP, WebP

## 🎨 Frontend Technology Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **UI Components**: 
  - [Shadcn UI](https://ui.shadcn.com/) - Reusable component library
  - [Aceternity UI](https://ui.aceternity.com/) - Animated components with Framer Motion
- **State Management**: React Context API
- **TypeScript**: Full type safety

### Key Frontend Features

- **Responsive Design**: Mobile-first responsive interface
- **Dark/Light Mode**: Theme switching capability
- **File Upload**: Drag-and-drop file upload interface
- **Real-time Updates**: Processing status tracking
- **Animations**: Smooth transitions and micro-interactions

## 🔧 Development Setup

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Initialize Qdrant with seed data
bun run init-qdrant

# Start development server with hot reload
python app.py
```

### Frontend Development

```bash
cd frontend

# Install dependencies
bun install

# Start development server with hot reload
bun dev
```

### Adding New UI Components

For Shadcn UI components:
```bash
cd frontend
npx shadcn-ui@latest add <component-name>
```

## 🚀 Production Deployment

### Backend Production

```bash
cd backend

# Install production dependencies
pip install gunicorn

# Start production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend Production

```bash
cd frontend

# Build for production
bun run build

# Start production server
bun start
```

### Docker Deployment

Both services can be containerized:

```bash
# Backend
cd backend
docker build -t qdrant-hackathon-backend .

# Frontend
cd frontend
docker build -t qdrant-hackathon-frontend .
```

## 🧠 Vector Database Integration

The platform leverages Qdrant for intelligent music recommendations:

1. **Song Embeddings**: Metadata converted to vector embeddings using sentence transformers
2. **Semantic Search**: Find similar songs based on text queries or uploaded content
3. **Personalized Recommendations**: AI-powered suggestions using vector similarity
4. **Real-time Processing**: Fast similarity search with sub-second response times

## 📁 Project Structure

### Backend Structure
```
backend/
├── app/
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
└── app.py                  # Application entry point
```

### Frontend Structure
```
frontend/
├── app/                     # Next.js app directory
├── components/              # React components
│   ├── ui/                 # Shadcn/Aceternity UI components
│   ├── create/             # Creation flow components
│   └── ...
├── context/                # React context providers
├── hooks/                  # Custom React hooks
└── lib/                   # Utility functions
```

## 🔐 Environment Configuration

### Backend (.env)
```bash
QDRANT_HOST=localhost
QDRANT_PORT=6333
CORS_ORIGINS=http://localhost:3000
MAX_CONTENT_LENGTH=104857600  # 100MB
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
bun run test
```

### Frontend Tests
```bash
cd frontend
bun test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -m 'Add some amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Hackathon Goals

This project was developed for the Qdrant Hackathon 2025 with the following objectives:

- Demonstrate practical applications of vector databases in creative industries
- Showcase semantic search capabilities for music recommendation
- Build a user-friendly interface for complex AI-powered functionality
- Create a scalable architecture for multimedia processing

---

**Built with ❤️ for Qdrant Hackathon 2025**
