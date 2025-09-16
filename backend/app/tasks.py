from app.extensions import celery
import time
import logging
import os
import tempfile
import hashlib
from qdrant_client.models import PointStruct
from app.services.recommendation_service import RecommendationService
from app.services.video_analysis_service import VideoAnalysisService
from app.services.music_vectorization_service import MusicVectorizationService
from config.config import Config

logger = logging.getLogger(__name__)

@celery.task(bind=True, name='create_task')
def create_task(self, video_id):
    """
    Process a YouTube video by downloading its audio and vectorizing it.
    
    Args:
        video_id (str): The YouTube video ID to process
        
    Returns:
        dict: Task completion status with processing details
    """
    collection_name = Config.QDRANT_COLLECTION_NAME
    # Initialize task metadata
    start_time = time.strftime('%Y-%m-%d %H:%M:%S')
    temp_dir = None
    audio_path = None
    
    task_meta = {
        'video_id': video_id,
        'start_time': start_time,
        'status': 'STARTED',
        'progress': 0,
        'total_steps': 4,  # Download, Extract, Vectorize, Store
        'current_step': 0,
        'message': 'Initializing...'
    }
    
    def update_progress(step, message, progress=None):
        nonlocal task_meta
        task_meta.update({
            'current_step': step,
            'message': message,
            'progress': progress if progress is not None else (step / task_meta['total_steps']) * 100,
            'status': 'PROCESSING',
            'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        self.update_state(state='PROGRESS', meta=task_meta)
    
    try:
        # Initialize services
        update_progress(0, 'Initializing MusicVectorizationService...')
        try:
            vectorization_service = MusicVectorizationService()
        except Exception as e:
            logger.error(f"Failed to initialize MusicVectorizationService: {str(e)}")
            raise Exception(f"Service initialization failed: {str(e)}")
        
        # Step 1: Download audio
        update_progress(1, 'Downloading audio from YouTube...', 25)
        try:
            temp_dir = tempfile.mkdtemp()
            audio_path = vectorization_service.download_audio(video_id, temp_dir)
            update_progress(1, f'Audio downloaded to {audio_path}', 25)
        except Exception as e:
            logger.error(f"Error downloading audio: {str(e)}")
            raise Exception(f"Failed to download audio: {str(e)}")
        
        # Step 2: Extract audio features
        update_progress(2, 'Extracting audio features...', 50)
        try:
            features = vectorization_service.extract_audio_features(audio_path)
            update_progress(2, f'Extracted {len(features)}-dim audio features', 50)
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            raise Exception(f"Failed to extract audio features: {str(e)}")
        
        # Step 3: Store in Qdrant
        update_progress(3, 'Storing vector in Qdrant...', 75)
        try:
            # Create a point ID from video_id
            point_id = int(hashlib.sha256(video_id.encode('utf-8')).hexdigest()[:16], 16)
            
            # Store the vector
            try:
                vectorization_service.qdrant_client.upsert(
                    collection_name=vectorization_service.collection_name,
                    points=[
                        PointStruct(
                            id=point_id,
                            vector=features,
                            payload={
                                'video_id': video_id,
                                'source': 'youtube',
                                'processed_at': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                                'vector_dim': len(features),
                                'collection': vectorization_service.collection_name
                            }
                        )
                    ]
                )
            except Exception as e:
                logger.error(f"Failed to store vector in Qdrant: {str(e)}")
                raise Exception(f"Vector storage failed: {str(e)}")
            update_progress(3, f'Vector stored in Qdrant collection: {vectorization_service.collection_name}', 75)
        except Exception as e:
            logger.error(f"Error storing in Qdrant: {str(e)}")
            raise Exception(f"Failed to store vector in Qdrant: {str(e)}")
        
        # Task completion
        end_time = time.strftime('%Y-%m-%d %H:%M:%S')
        duration = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')) - \
                  time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        
        result = {
            'status': 'COMPLETED',
            'video_id': video_id,
            'collection': vectorization_service.collection_name,
            'vector_dim': len(features),
            'start_time': start_time,
            'end_time': end_time,
            'duration_seconds': round(duration, 2),
            'message': 'Video processed and vectorized successfully',
            'vector_id': str(point_id),
            'vector_size': len(features)
        }
        
        return result
        
    except Exception as e:
        logger.error(f"Error in create_task for video {video_id}: {str(e)}", exc_info=True)
        end_time = time.strftime('%Y-%m-%d %H:%M:%S')
        duration = time.time() - time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        
        # Format the exception info according to Celery's expected format
        exc_type = type(e).__name__
        exc_message = str(e)
        
        error_result = {
            'exc_type': exc_type,
            'exc_message': exc_message,
            'exc_module': e.__class__.__module__,
            'status': 'FAILURE',
            'video_id': video_id,
            'start_time': start_time,
            'end_time': end_time,
            'duration_seconds': round(duration, 2),
            'current_step': task_meta.get('current_step', 0),
            'total_steps': task_meta.get('total_steps', 4),
            'progress': task_meta.get('progress', 0),
            'message': f'Task failed: {exc_type}: {exc_message}'
        }
        
        try:
            # Update the task state with the error information
            self.update_state(
                state='FAILURE',
                meta=error_result
            )
        except Exception as update_err:
            logger.error(f"Failed to update task state: {str(update_err)}", exc_info=True)
            # If we can't update the state, at least log the full error
            logger.error(f"Original error: {exc_type}: {exc_message}", exc_info=True)
        
        # Re-raise the original exception with proper type
        raise type(e)(str(e)) from e
    
    finally:
        # Cleanup temporary files
        if audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
                if temp_dir and os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
            except Exception as e:
                logger.warning(f"Error cleaning up temporary files: {str(e)}")

@celery.task(bind=True, name='analyze_video_and_recommend')
def analyze_video_and_recommend(self, video_path, limit=10):
    """
    Analyze a video and generate music recommendations
    
    Args:
        video_path (str): Path to the video file to analyze
        limit (int): Maximum number of recommendations to return
        
    Returns:
        dict: Analysis results and recommendations
    """
    try:
        # Initialize services
        vectorization_service = MusicVectorizationService()
        
        # 1. Extract features from video
        features = vectorization_service.extract_audio_features(video_path)
        
        # 2. Get recommendations
        recommendations = vectorization_service.search_similar(
            vector=features,
            limit=limit
        )
        
        return {
            'status': 'SUCCESS',
            'recommendations': recommendations,
            'features_extracted': len(features) > 0
        }
    except Exception as e:
        logger.error(f"Error in analyze_video: {str(e)}", exc_info=True)
        error_info = {
            'exc_type': type(e).__name__,
            'exc_message': str(e),
            'exc_module': e.__class__.__module__
        }
        try:
            self.update_state(state='FAILURE', meta={'error': error_info})
        except Exception as update_err:
            logger.error(f"Failed to update task state: {str(update_err)}")
        raise type(e)(str(e)) from e

@celery.task(bind=True, name='initialize_music_database')
def initialize_music_database(self, max_videos=50):
    """
    Initialize the music database with trending videos
    
    Args:
        max_videos (int): Maximum number of trending videos to process
        
    Returns:
        dict: Initialization status and statistics
    """
    try:
        vectorization_service = MusicVectorizationService()
        
        # 1. Get trending videos (this would come from your data service)
        # For now, we'll just return a placeholder
        result = {
            'processed': 0,
            'failed': 0,
            'total': max_videos
        }
        
        return {
            'status': 'SUCCESS',
            'result': result,
            'message': f'Database initialized with {max_videos} trending videos'
        }
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}", exc_info=True)
        error_info = {
            'exc_type': type(e).__name__,
            'exc_message': str(e),
            'exc_module': e.__class__.__module__
        }
        try:
            self.update_state(state='FAILURE', meta={'error': error_info})
        except Exception as update_err:
            logger.error(f"Failed to update task state: {str(update_err)}")
        raise type(e)(str(e)) from e