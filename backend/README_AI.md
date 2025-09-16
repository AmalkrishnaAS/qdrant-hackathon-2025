# AI-Powered Music Recommendation System

This document describes the AI-powered music recommendation system implemented in the backend, featuring video analysis with Gemini AI and music vectorization with CLAP models.

## Overview

The system combines three key AI technologies:

1. **Google Gemini AI** - For intelligent video content analysis
2. **CLAP Models** - For music and text vectorization
3. **Qdrant Vector Database** - For semantic similarity search

## Architecture

```
Video Upload → Gemini Analysis → Text Query → CLAP Vectorization → Qdrant Search → Music Recommendations
```

## AI Services

### 1. Video Analysis Service (`video_analysis_service.py`)

Uses Google Gemini AI to analyze video content and generate detailed descriptions for music matching.

**Features:**
- Content and narrative analysis
- Visual style and atmosphere detection
- Emotional tone recognition
- Music genre and tempo suggestions

**Usage:**
```python
from app.services.video_analysis_service import VideoAnalysisService

analyzer = VideoAnalysisService(api_key="your-gemini-key")
analysis = analyzer.analyze_video("path/to/video.mp4")
```

**Output Format:**
```json
{
  "description": "A energetic video featuring fast-paced action...",
  "music_recommendation": "Upbeat electronic dance music",
  "keywords": ["energetic", "fast-paced", "electronic"],
  "mood": "energetic",
  "genre_suggestions": ["electronic", "dance", "pop"],
  "tempo": "Fast",
  "energy_level": "High"
}
```

### 2. Music Vectorization Service (`music_vectorization_service.py`)

Uses CLAP (Contrastive Language-Audio Pretraining) models to create embeddings from both audio and text.

**Features:**
- Audio feature extraction from music files
- Text-to-audio embedding for semantic search
- YouTube integration for trending music discovery
- Qdrant vector storage and retrieval

**Usage:**
```python
from app.services.music_vectorization_service import MusicVectorizationService

music_service = MusicVectorizationService()

# Extract features from audio
features = music_service.extract_audio_features("audio.mp3")

# Search with text query
results = music_service.search_similar_music("upbeat electronic music")
```

### 3. Recommendation Service (`recommendation_service.py`)

Combines video analysis with music search for intelligent recommendations.

**Features:**
- Video-to-music recommendation pipeline
- Text-based music search
- Trending music discovery
- Database initialization and management

**Usage:**
```python
from app.services.recommendation_service import RecommendationService

rec_service = RecommendationService()

# Analyze video and get recommendations
analysis, songs = rec_service.analyze_video_and_recommend("video.mp4")

# Text-based recommendations
songs = rec_service.recommend_by_text_query("calm ambient music")
```

## API Endpoints

### Video Analysis

```http
POST /api/recommendations/analyze-video
Content-Type: multipart/form-data

video: (file)
limit: 10
```

**Response:**
```json
{
  "success": true,
  "task_id": "task-uuid",
  "message": "Video analysis started"
}
```

### Text Recommendations

```http
POST /api/recommendations/text-recommendations
Content-Type: application/json

{
  "query": "energetic workout music",
  "limit": 10
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "song-uuid",
      "title": "Song Title",
      "artists": ["Artist Name"],
      "album": "Album Name",
      "duration": "3:45",
      "videoId": "youtube-id",
      "thumbnails": {...}
    }
  ],
  "total": 10
}
```

### Database Initialization

```http
POST /api/recommendations/initialize-database
Content-Type: application/json

{
  "max_videos": 50
}
```

**Response:**
```json
{
  "success": true,
  "task_id": "task-uuid",
  "message": "Database initialization started"
}
```

### Database Statistics

```http
GET /api/recommendations/database-stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "collection_name": "youtube_audio_vectors",
    "vectors_count": 1250,
    "points_count": 1250,
    "status": "green"
  }
}
```

## Background Tasks

The system uses Celery for long-running AI operations:

### Video Analysis Task

```python
@celery.task(bind=True, name='analyze_video_and_recommend')
def analyze_video_and_recommend(self, video_path, limit=10):
    # 1. Initialize services
    # 2. Analyze video with Gemini
    # 3. Generate music recommendations
    # 4. Return results
```

### Database Initialization Task

```python
@celery.task(bind=True, name='initialize_music_database')
def initialize_music_database(self, max_videos=50):
    # 1. Fetch trending YouTube videos
    # 2. Download and process audio
    # 3. Generate CLAP embeddings
    # 4. Store in Qdrant
```

## Configuration

### Environment Variables

```env
# AI Service API Keys
GEMINI_API_KEY=your-gemini-api-key
YOUTUBE_API_KEY=your-youtube-api-key

# Model Configuration
CLAP_MODEL_NAME=laion/clap-htsat-unfused

# Qdrant Configuration
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_API_KEY=optional-api-key
```

### Model Requirements

- **CLAP Model**: ~2GB download, requires significant RAM/VRAM
- **Gemini API**: Requires active Google Cloud project with billing
- **YouTube API**: Free tier available with quotas

## Performance Considerations

### Memory Usage
- CLAP models require 4-8GB RAM minimum
- GPU acceleration recommended for faster inference
- Consider model quantization for resource-constrained environments

### API Quotas
- **Gemini API**: Monitor usage and implement rate limiting
- **YouTube API**: 10,000 units/day free tier
- **Qdrant**: No limits for self-hosted instances

### Optimization Tips

1. **Batch Processing**: Process multiple videos together
2. **Caching**: Cache embeddings for frequently accessed content
3. **Model Loading**: Load models once and reuse across requests
4. **Async Processing**: Use Celery for long-running operations

## Testing

### Test Script

```bash
# Run comprehensive AI service tests
python test_music_db.py
```

### Manual Testing

```bash
# Test video analysis
curl -X POST "http://localhost:5000/api/recommendations/analyze-video" \
  -F "video=@test_video.mp4"

# Test text recommendations
curl -X POST "http://localhost:5000/api/recommendations/text-recommendations" \
  -H "Content-Type: application/json" \
  -d '{"query": "upbeat pop music"}'

# Initialize database
curl -X POST "http://localhost:5000/api/recommendations/initialize-database" \
  -H "Content-Type: application/json" \
  -d '{"max_videos": 20}'
```

## Troubleshooting

### Common Issues

1. **Model Download Failures**
   - Ensure stable internet connection
   - Check available disk space (>5GB recommended)
   - Verify Hugging Face access

2. **API Key Errors**
   - Verify Gemini API key is valid and has quota
   - Check YouTube API key permissions
   - Ensure APIs are enabled in Google Cloud Console

3. **Memory Issues**
   - Monitor RAM usage during model loading
   - Consider using smaller CLAP models
   - Implement model offloading for resource-constrained environments

4. **Qdrant Connection Issues**
   - Verify Qdrant server is running
   - Check network connectivity
   - Ensure collection is properly initialized

### Performance Monitoring

```python
# Monitor model performance
import time
import psutil

def monitor_inference():
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    # Run inference
    result = model.inference(data)
    
    end_time = time.time()
    end_memory = psutil.virtual_memory().used
    
    print(f"Inference time: {end_time - start_time:.2f}s")
    print(f"Memory usage: {(end_memory - start_memory) / 1024**2:.2f}MB")
```

## Future Enhancements

1. **Multi-Modal Analysis**: Combine audio, video, and text analysis
2. **Real-Time Processing**: Stream processing for live video
3. **Custom Model Training**: Fine-tune models on domain-specific data
4. **Advanced Filtering**: Genre, mood, and tempo-based filtering
5. **User Personalization**: Learn from user preferences and behavior

## Contributing

When contributing to the AI services:

1. **Test Thoroughly**: AI models can be unpredictable
2. **Monitor Resources**: Track memory and compute usage
3. **Document Changes**: Update API documentation
4. **Consider Fallbacks**: Implement graceful degradation
5. **Validate Outputs**: Ensure AI outputs are reasonable

## License

MIT License - see main LICENSE file for details.
