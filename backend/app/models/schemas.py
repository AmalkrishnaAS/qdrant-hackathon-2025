from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class Thumbnail(BaseModel):
    """Thumbnail model matching frontend structure"""
    url: str
    width: int
    height: int

class Thumbnails(BaseModel):
    """Collection of thumbnails"""
    default: Thumbnail
    medium: Thumbnail
    high: Thumbnail

class Song(BaseModel):
    """Song/Track model matching frontend Item interface"""
    id: str
    title: str
    artists: List[str]
    album: str
    duration: str
    thumbnails: Thumbnails
    videoId: str
    isExplicit: bool = False
    category: str
    description: str
    audioUrl: Optional[str] = None
    createdAt: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SongResponse(BaseModel):
    """Response model for song endpoints"""
    success: bool = True
    data: List[Song]
    message: Optional[str] = None
    total: Optional[int] = None

class SingleSongResponse(BaseModel):
    """Response model for single song endpoint"""
    success: bool = True
    data: Song
    message: Optional[str] = None

class FileUpload(BaseModel):
    """File upload model"""
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    upload_path: str
    created_at: datetime = Field(default_factory=datetime.now)

class UploadResponse(BaseModel):
    """Response model for file upload"""
    success: bool = True
    data: FileUpload
    message: Optional[str] = None

class RecommendationRequest(BaseModel):
    """Request model for getting recommendations"""
    uploaded_files: Optional[List[str]] = []
    query: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=50)
    include_metadata: bool = True

class RecommendationResponse(BaseModel):
    """Response model for recommendations"""
    success: bool = True
    data: List[Song]
    message: Optional[str] = None
    query_info: Optional[Dict[str, Any]] = None

class ProcessRequest(BaseModel):
    """Request model for processing video with audio"""
    video_file: str
    selected_track_id: str
    start_time: Optional[float] = 0.0
    end_time: Optional[float] = None
    output_format: str = Field(default="mp4")

class ProcessResponse(BaseModel):
    """Response model for video processing"""
    success: bool = True
    data: Dict[str, str]  # Contains download_url, file_id, etc.
    message: Optional[str] = None
    processing_id: Optional[str] = None

class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
    services: Dict[str, bool] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

