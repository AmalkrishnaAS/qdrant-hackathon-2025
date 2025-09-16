import logging
import os
from typing import List, Dict, Optional, Any, Tuple
from .video_analysis_service import VideoAnalysisService
from .music_vectorization_service import MusicVectorizationService
from app.models.schemas import Song, Thumbnail, Thumbnails
import tempfile
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service that combines video analysis with music recommendation"""
    
    def __init__(
        self,
        gemini_api_key: Optional[str] = None,
        youtube_api_key: Optional[str] = None,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        qdrant_api_key: Optional[str] = None
    ):
        """Initialize the recommendation service"""
        self.gemini_api_key = gemini_api_key or os.environ.get("GEMINI_API_KEY")
        self.youtube_api_key = youtube_api_key or os.environ.get("YOUTUBE_API_KEY")
        
        if not self.gemini_api_key:
            logger.warning("GEMINI_API_KEY not provided - video analysis will be disabled")
            self.video_analyzer = None
        else:
            self.video_analyzer = VideoAnalysisService(self.gemini_api_key)
        
        if not self.youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not provided - some features may be limited")
        
        # Initialize music vectorization service
        self.music_service = MusicVectorizationService(
            qdrant_host=qdrant_host,
            qdrant_port=qdrant_port,
            qdrant_api_key=qdrant_api_key
        )
    
    def analyze_video_and_recommend(
        self, 
        video_path: str, 
        limit: int = 10
    ) -> Tuple[Dict[str, Any], List[Song]]:
        """
        Analyze a video and recommend matching music
        
        Returns:
            Tuple of (video_analysis, recommended_songs)
        """
        try:
            if not self.video_analyzer:
                raise ValueError("Video analysis not available - GEMINI_API_KEY required")
            
            # Analyze video
            logger.info(f"Analyzing video: {video_path}")
            video_analysis = self.video_analyzer.analyze_video(video_path)
            
            # Generate search query from analysis
            search_query = self.video_analyzer.generate_search_query(video_analysis)
            
            # Search for matching music
            logger.info(f"Searching for music with query: {search_query}")
            music_results = self.music_service.search_similar_music(search_query, limit=limit)
            
            # Convert to Song objects
            songs = self._convert_music_results_to_songs(music_results)
            
            logger.info(f"Generated {len(songs)} music recommendations for video")
            return video_analysis, songs
            
        except Exception as e:
            logger.error(f"Error in video analysis and recommendation: {e}")
            raise
    
    def recommend_by_text_query(self, query: str, limit: int = 10) -> List[Song]:
        """Recommend music based on text query"""
        try:
            logger.info(f"Getting music recommendations for text query: {query}")
            
            # Search for matching music
            music_results = self.music_service.search_similar_music(query, limit=limit)
            
            # Convert to Song objects
            songs = self._convert_music_results_to_songs(music_results)
            
            logger.info(f"Generated {len(songs)} recommendations for text query")
            return songs
            
        except Exception as e:
            logger.error(f"Error getting text-based recommendations: {e}")
            raise
    
    def get_trending_recommendations(self, limit: int = 10) -> List[Song]:
        """Get trending music recommendations"""
        try:
            logger.info("Getting trending music recommendations")
            
            # Use a trending-focused query
            trending_query = "popular trending hit songs music viral"
            music_results = self.music_service.search_similar_music(trending_query, limit=limit)
            
            # Convert to Song objects
            songs = self._convert_music_results_to_songs(music_results)
            
            logger.info(f"Generated {len(songs)} trending recommendations")
            return songs
            
        except Exception as e:
            logger.error(f"Error getting trending recommendations: {e}")
            # Return empty list as fallback
            return []
    
    def initialize_music_database(self, max_videos: int = 50) -> Dict[str, int]:
        """Initialize the music database with trending videos"""
        try:
            if not self.youtube_api_key:
                raise ValueError("YouTube API key required for database initialization")
            
            logger.info(f"Initializing music database with {max_videos} videos")
            result = self.music_service.process_trending_videos(
                self.youtube_api_key, 
                max_results=max_videos
            )
            
            logger.info(f"Database initialization complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error initializing music database: {e}")
            raise
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get statistics about the music database"""
        return self.music_service.get_collection_stats()
    
    def _convert_music_results_to_songs(self, music_results: List[Dict[str, Any]]) -> List[Song]:
        """Convert music search results to Song objects"""
        songs = []
        
        for result in music_results:
            try:
                # Create thumbnail objects
                thumbnail_url = result.get("thumbnail", "")
                if not thumbnail_url:
                    # Use a default thumbnail
                    thumbnail_url = "https://img.youtube.com/vi/default/default.jpg"
                
                # Create thumbnail with different sizes (YouTube standard)
                video_id = result.get("video_id", "")
                if video_id:
                    default_thumb = Thumbnail(
                        url=f"https://img.youtube.com/vi/{video_id}/default.jpg",
                        width=120,
                        height=90
                    )
                    medium_thumb = Thumbnail(
                        url=f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg",
                        width=320,
                        height=180
                    )
                    high_thumb = Thumbnail(
                        url=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                        width=480,
                        height=360
                    )
                else:
                    # Fallback thumbnails
                    default_thumb = medium_thumb = high_thumb = Thumbnail(
                        url=thumbnail_url,
                        width=320,
                        height=180
                    )
                
                thumbnails = Thumbnails(
                    default=default_thumb,
                    medium=medium_thumb,
                    high=high_thumb
                )
                
                # Extract artist from channel title or title
                title = result.get("title", "Unknown Title")
                channel_title = result.get("channelTitle", "Unknown Artist")
                
                # Try to extract artist from title (common format: "Artist - Song")
                if " - " in title:
                    parts = title.split(" - ", 1)
                    if len(parts) == 2:
                        artists = [parts[0].strip()]
                        song_title = parts[1].strip()
                    else:
                        artists = [channel_title]
                        song_title = title
                else:
                    artists = [channel_title]
                    song_title = title
                
                # Create Song object
                song = Song(
                    id=str(uuid.uuid4()),
                    title=song_title,
                    artists=artists,
                    album=channel_title,  # Use channel as album
                    duration=self._format_duration(result.get("duration", "")),
                    thumbnails=thumbnails,
                    videoId=video_id,
                    isExplicit=False,  # YouTube doesn't provide this directly
                    category="Music",
                    description=result.get("description", "")[:200],  # Truncate description
                    audioUrl=f"https://www.youtube.com/watch?v={video_id}" if video_id else None,
                    createdAt=datetime.now()
                )
                
                songs.append(song)
                
            except Exception as e:
                logger.warning(f"Error converting music result to Song: {e}")
                continue
        
        return songs
    
    def _format_duration(self, duration: str) -> str:
        """Format YouTube duration to a readable format"""
        if not duration:
            return "0:00"
        
        # YouTube duration format is PT#M#S or PT#H#M#S
        try:
            import re
            
            # Remove PT prefix
            duration = duration.replace("PT", "")
            
            # Extract hours, minutes, seconds
            hours = 0
            minutes = 0
            seconds = 0
            
            hour_match = re.search(r'(\d+)H', duration)
            if hour_match:
                hours = int(hour_match.group(1))
            
            minute_match = re.search(r'(\d+)M', duration)
            if minute_match:
                minutes = int(minute_match.group(1))
            
            second_match = re.search(r'(\d+)S', duration)
            if second_match:
                seconds = int(second_match.group(1))
            
            # Format as MM:SS or HH:MM:SS
            if hours > 0:
                return f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes}:{seconds:02d}"
                
        except Exception:
            return "0:00"
