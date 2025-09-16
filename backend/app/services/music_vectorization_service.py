import os
import uuid
import numpy as np
import torch
import librosa
import yt_dlp
import hashlib
import logging
from typing import List, Dict, Optional, Any, Tuple
from transformers import AutoProcessor, ClapModel
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from googleapiclient.discovery import build
from pathlib import Path
import tempfile
from config.config import Config

logger = logging.getLogger(__name__)

class MusicVectorizationService:
    """Service for vectorizing music using CLAP models and storing in Qdrant"""
    
    def __init__(
        self, 
        model_name: str = "laion/clap-htsat-unfused",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        qdrant_api_key: Optional[str] = None
    ):
        """Initialize the music vectorization service"""
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.target_sr = 48000
        # Match dimension with Qdrant collection (all-MiniLM-L6-v2 uses 384 dimensions)
        self.vector_dim = 384
        
        # Initialize CLAP model
        try:
            self.processor = AutoProcessor.from_pretrained(model_name)
            self.model = ClapModel.from_pretrained(model_name).to(self.device).eval()
            logger.info(f"CLAP model {model_name} loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load CLAP model: {e}")
            raise
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            host=qdrant_host, 
            port=qdrant_port, 
            api_key=qdrant_api_key
        )
        self.collection_name = Config.QDRANT_COLLECTION_NAME
        
        # Ensure collection exists
        self._ensure_collection_exists()
        
    def _ensure_collection_exists(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            if not self.qdrant_client.collection_exists(self.collection_name):
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_dim, 
                        distance=Distance.COSINE
                    ),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
            else:
                logger.info(f"Qdrant collection {self.collection_name} already exists")
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def download_audio(self, video_id: str, output_path: Optional[str] = None) -> str:
        """Download audio from YouTube video"""
        if output_path is None:
            output_path = tempfile.mkdtemp()
        
        os.makedirs(output_path, exist_ok=True)
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{output_path}/%(id)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
            "no_warnings": True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                audio_path = os.path.join(output_path, f"{video_id}.mp3")
                
                if os.path.exists(audio_path):
                    logger.info(f"Downloaded audio for video {video_id}")
                    return audio_path
                else:
                    raise FileNotFoundError(f"Downloaded file not found: {audio_path}")
                    
        except Exception as e:
            logger.error(f"Error downloading audio for {video_id}: {e}")
            raise
    
    def extract_audio_features(self, file_path: str) -> List[float]:
        """Extract audio features using CLAP model"""
        try:
            # Load audio file
            waveform, _ = librosa.load(file_path, sr=self.target_sr, mono=True)
            
            # Process with CLAP
            inputs = self.processor(
                audios=waveform, 
                sampling_rate=self.target_sr, 
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                embedding = self.model.get_audio_features(**inputs)
            
            # Convert to list
            features = embedding.cpu().numpy().squeeze().tolist()
            logger.info(f"Extracted {len(features)}-dim audio features from {file_path}")
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting features from {file_path}: {e}")
            raise
    
    def extract_text_features(self, text: str) -> List[float]:
        """Extract text features using CLAP model for text-to-audio search"""
        try:
            inputs = self.processor(text=[text], return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                embedding = self.model.get_text_features(**inputs)
            
            features = embedding.cpu().numpy().squeeze().tolist()
            logger.info(f"Extracted text features for: {text[:50]}...")
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting text features: {e}")
            raise
    
    def get_youtube_metadata(self, video_id: str, api_key: str) -> Dict[str, Any]:
        """Get metadata for a YouTube video"""
        try:
            youtube = build("youtube", "v3", developerKey=api_key)
            response = youtube.videos().list(
                part="snippet,contentDetails,statistics", 
                id=video_id
            ).execute()
            
            if not response["items"]:
                return {"error": "Video not found"}
            
            video = response["items"][0]
            metadata = {
                "title": video["snippet"]["title"],
                "description": video["snippet"]["description"],
                "channelTitle": video["snippet"]["channelTitle"],
                "publishedAt": video["snippet"]["publishedAt"],
                "duration": video["contentDetails"]["duration"],
                "views": video["statistics"].get("viewCount"),
                "likes": video["statistics"].get("likeCount"),
                "comments": video["statistics"].get("commentCount"),
                "tags": video["snippet"].get("tags", []),
                "thumbnail": video["snippet"]["thumbnails"]["high"]["url"],
            }
            
            logger.info(f"Retrieved metadata for video {video_id}: {metadata['title']}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error getting YouTube metadata for {video_id}: {e}")
            return {"error": str(e)}
    
    def store_in_qdrant(self, video_id: str, vector: List[float], metadata: Dict[str, Any]) -> bool:
        """Store audio vector and metadata in Qdrant"""
        try:
            # Generate consistent numeric ID from video_id
            point_id = int(hashlib.sha256(video_id.encode()).hexdigest()[:16], 16) % (2**63)
            
            # Prepare point
            point = PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "video_id": video_id,
                    "source": "youtube",
                    **metadata
                }
            )
            
            # Upsert to Qdrant
            self.qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point],
                wait=True
            )
            
            logger.info(f"Stored vector for {video_id} in Qdrant")
            return True
            
        except Exception as e:
            logger.error(f"Error storing in Qdrant: {e}")
            return False
    
    def process_single_video(self, video_id: str, youtube_api_key: str) -> bool:
        """Process a single video: download, vectorize, and store"""
        temp_dir = None
        try:
            logger.info(f"Processing video: {video_id}")
            
            # Get metadata
            metadata = self.get_youtube_metadata(video_id, youtube_api_key)
            if "error" in metadata:
                logger.error(f"Error getting metadata: {metadata['error']}")
                return False
            
            # Download audio
            temp_dir = tempfile.mkdtemp()
            audio_path = self.download_audio(video_id, temp_dir)
            
            # Extract features
            vector = self.extract_audio_features(audio_path)
            
            # Store in Qdrant
            success = self.store_in_qdrant(video_id, vector, metadata)
            
            if success:
                logger.info(f"✅ Successfully processed {video_id}: {metadata.get('title', '')}")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error processing video {video_id}: {e}")
            return False
            
        finally:
            # Cleanup temporary files
            if temp_dir and os.path.exists(temp_dir):
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                    logger.debug(f"Cleaned up temp directory: {temp_dir}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp directory: {e}")
    
    def get_trending_videos(self, youtube_api_key: str, region_code: str = "US", max_results: int = 50) -> List[str]:
        """Get trending music video IDs from YouTube"""
        try:
            youtube = build("youtube", "v3", developerKey=youtube_api_key)
            
            request = youtube.videos().list(
                part="id",
                chart="mostPopular",
                regionCode=region_code,
                maxResults=min(max_results, 50),
                videoCategoryId="10"  # Music category
            )
            
            response = request.execute()
            video_ids = [item['id'] for item in response.get('items', [])]
            
            logger.info(f"Found {len(video_ids)} trending videos in {region_code}")
            return video_ids
            
        except Exception as e:
            logger.error(f"Error fetching trending videos: {e}")
            return []
    
    def process_trending_videos(self, youtube_api_key: str, max_results: int = 20) -> Dict[str, int]:
        """Process trending videos and store in Qdrant"""
        logger.info(f"Processing up to {max_results} trending videos...")
        
        # Get trending video IDs
        video_ids = self.get_trending_videos(youtube_api_key, max_results=max_results)
        
        if not video_ids:
            logger.warning("No trending videos found")
            return {"processed": 0, "failed": 0}
        
        # Process each video
        processed = 0
        failed = 0
        
        for video_id in video_ids[:max_results]:
            try:
                if self.process_single_video(video_id, youtube_api_key):
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Failed to process video {video_id}: {e}")
                failed += 1
        
        result = {"processed": processed, "failed": failed}
        logger.info(f"Processing complete: {result}")
        return result
    
    def search_similar_music(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for similar music using text query"""
        try:
            # Extract text features
            query_vector = self.extract_text_features(query)
            
            # Search in Qdrant
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            
            # Convert results
            results = []
            for hit in search_result:
                result = {
                    "id": str(hit.id),
                    "score": hit.score,
                    "video_id": hit.payload.get("video_id"),
                    "title": hit.payload.get("title"),
                    "channelTitle": hit.payload.get("channelTitle"),
                    "thumbnail": hit.payload.get("thumbnail"),
                    "duration": hit.payload.get("duration"),
                    "views": hit.payload.get("views"),
                    **hit.payload
                }
                results.append(result)
            
            logger.info(f"Found {len(results)} similar tracks for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching similar music: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the music collection"""
        try:
            info = self.qdrant_client.get_collection(self.collection_name)
            return {
                "collection_name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status.name if info.status else "unknown"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
