import logging
from typing import List, Dict, Optional, Any
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance, VectorParams, CreateCollection, PointStruct, 
    Filter, FieldCondition, SearchRequest, CollectionStatus
)
from qdrant_client.http.exceptions import UnexpectedResponse
from sentence_transformers import SentenceTransformer
from app.models.schemas import Song
import uuid

logger = logging.getLogger(__name__)

class QdrantService:
    """Service for interacting with Qdrant vector database"""
    
    def __init__(self, host: str = "localhost", port: int = 6333, api_key: Optional[str] = None):
        # Use HTTP for localhost, HTTPS for remote hosts
        prefer_grpc = False
        https = False if host in ['localhost', '127.0.0.1'] else True
        self.client = QdrantClient(host=host, port=port, api_key=api_key, prefer_grpc=prefer_grpc, https=https)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight model for embeddings
        self.collection_name = "music_embeddings"
        self.vector_size = self.encoder.get_sentence_embedding_dimension()
        
        # Initialize collection
        self._ensure_collection_exists()
    
    def _ensure_collection_exists(self):
        """Create collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            if self.collection_name not in collection_names:
                logger.info(f"Creating collection: {self.collection_name}")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info("Collection created successfully")
            else:
                logger.info(f"Collection {self.collection_name} already exists")
                
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {e}")
            raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text using sentence transformer"""
        try:
            embedding = self.encoder.encode(text)
            return embedding.astype(np.float32)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
    
    def generate_song_text(self, song: Song) -> str:
        """Generate searchable text from song metadata"""
        text_parts = [
            song.title,
            ' '.join(song.artists),
            song.album,
            song.category,
            song.description
        ]
        return ' '.join(filter(None, text_parts))
    
    def add_song(self, song: Song) -> bool:
        """Add a song to the vector database"""
        try:
            # Generate text for embedding
            song_text = self.generate_song_text(song)
            embedding = self.generate_embedding(song_text)
            
            # Create point with UUID (Qdrant requirement)
            import uuid
            point = PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, song.id)),
                vector=embedding.tolist(),
                payload={
                    "title": song.title,
                    "artists": song.artists,
                    "album": song.album,
                    "duration": song.duration,
                    "videoId": song.videoId,
                    "isExplicit": song.isExplicit,
                    "category": song.category,
                    "description": song.description,
                    "thumbnails": song.thumbnails.dict() if song.thumbnails else None,
                    "audioUrl": song.audioUrl,
                    "searchText": song_text
                }
            )
            
            # Insert into Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Added song to Qdrant: {song.title}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding song to Qdrant: {e}")
            return False
    
    def add_songs_batch(self, songs: List[Song]) -> int:
        """Add multiple songs to the vector database"""
        added_count = 0
        points = []
        
        try:
            for song in songs:
                song_text = self.generate_song_text(song)
                embedding = self.generate_embedding(song_text)
                
                point = PointStruct(
                    id=str(uuid.uuid5(uuid.NAMESPACE_DNS, song.id)),
                    vector=embedding.tolist(),
                    payload={
                        "title": song.title,
                        "artists": song.artists,
                        "album": song.album,
                        "duration": song.duration,
                        "videoId": song.videoId,
                        "isExplicit": song.isExplicit,
                        "category": song.category,
                        "description": song.description,
                        "thumbnails": song.thumbnails.dict() if song.thumbnails else None,
                        "audioUrl": song.audioUrl,
                        "searchText": song_text
                    }
                )
                points.append(point)
            
            # Batch insert
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            added_count = len(points)
            logger.info(f"Added {added_count} songs to Qdrant")
            
        except Exception as e:
            logger.error(f"Error batch adding songs to Qdrant: {e}")
        
        return added_count
    
    def search_similar_songs(self, query: str, limit: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search for similar songs based on text query"""
        try:
            # Generate embedding for query
            query_embedding = self.generate_embedding(query)
            
            # Prepare filter if provided
            search_filter = None
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, list):
                        for v in value:
                            conditions.append(FieldCondition(key=key, match={"value": v}))
                    else:
                        conditions.append(FieldCondition(key=key, match={"value": value}))
                
                if conditions:
                    search_filter = Filter(should=conditions)
            
            # Perform search
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=limit,
                query_filter=search_filter,
                with_payload=True,
                with_vectors=False
            )
            
            # Convert results to list of dicts
            results = []
            for hit in search_result:
                result = {
                    "id": str(hit.id),
                    "score": hit.score,
                    **hit.payload
                }
                results.append(result)
            
            logger.info(f"Found {len(results)} similar songs for query: {query[:50]}...")
            return results
            
        except Exception as e:
            logger.error(f"Error searching similar songs: {e}")
            return []
    
    def search_by_categories(self, categories: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        """Search songs by categories"""
        try:
            conditions = [FieldCondition(key="category", match={"value": cat}) for cat in categories]
            search_filter = Filter(should=conditions)
            
            # Use a general query vector (could be improved)
            general_query = "popular music trending songs"
            query_embedding = self.generate_embedding(general_query)
            
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=limit,
                query_filter=search_filter,
                with_payload=True
            )
            
            results = []
            for hit in search_result:
                result = {
                    "id": str(hit.id),
                    "score": hit.score,
                    **hit.payload
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching by categories: {e}")
            return []
    
    def get_trending_songs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get trending songs (for now, just return random popular songs)"""
        try:
            # For now, search with a general "trending" query
            # In production, this could be based on play counts, recent additions, etc.
            trending_queries = ["popular hit songs", "trending music", "top charts"]
            
            all_results = []
            for query in trending_queries:
                results = self.search_similar_songs(query, limit=limit//len(trending_queries) + 1)
                all_results.extend(results)
            
            # Remove duplicates and limit results
            seen_ids = set()
            unique_results = []
            for result in all_results:
                if result["id"] not in seen_ids:
                    seen_ids.add(result["id"])
                    unique_results.append(result)
                    if len(unique_results) >= limit:
                        break
            
            return unique_results
            
        except Exception as e:
            logger.error(f"Error getting trending songs: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "status": info.status.name if info.status else "unknown",
                "points_count": info.points_count
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {"error": str(e)}
    
    def health_check(self) -> bool:
        """Check if Qdrant service is healthy"""
        try:
            collections = self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {e}")
            return False

