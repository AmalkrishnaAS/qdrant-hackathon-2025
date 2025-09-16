from app.extensions import celery
import time
import logging
import os
from app.services.recommendation_service import RecommendationService
from app.services.video_analysis_service import VideoAnalysisService
from app.services.music_vectorization_service import MusicVectorizationService

logger = logging.getLogger(__name__)

@celery.task(bind=True, name='create_task')
def create_task(self, video_id):
    """
    A mock task that simulates video processing.
    """
    total_steps = 10
    for i in range(total_steps):
        # Simulate work
        time.sleep(2)
        
        # Update state with progress
        progress = (i + 1) / total_steps * 100
        self.update_state(
            state='PROGRESS',
            meta={'current': i + 1, 'total': total_steps, 'percent': progress, 'video_id': video_id}
        )
    
    # Task completion
    return {'status': 'Completed', 'video_id': video_id, 'result_url': f'/static/processed/{video_id}.mp4'}

@celery.task(bind=True, name='analyze_video_and_recommend')
def analyze_video_and_recommend(self, video_path, limit=10):
    """
    Analyze a video and generate music recommendations
    """
    try:
        self.update_state(
            state='PROGRESS',
            meta={'current': 1, 'total': 4, 'percent': 25, 'status': 'Initializing services...'}
        )
        
        # Initialize recommendation service
        recommendation_service = RecommendationService()
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 2, 'total': 4, 'percent': 50, 'status': 'Analyzing video...'}
        )
        
        # Analyze video and get recommendations
        video_analysis, recommended_songs = recommendation_service.analyze_video_and_recommend(
            video_path, limit=limit
        )
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 3, 'total': 4, 'percent': 75, 'status': 'Processing recommendations...'}
        )
        
        # Convert songs to dict format for JSON serialization
        songs_data = [song.dict() for song in recommended_songs]
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 4, 'total': 4, 'percent': 100, 'status': 'Complete!'}
        )
        
        return {
            'status': 'Completed',
            'video_analysis': video_analysis,
            'recommendations': songs_data,
            'total_recommendations': len(songs_data)
        }
        
    except Exception as e:
        logger.error(f"Error in analyze_video_and_recommend task: {e}")
        return {
            'status': 'Failed',
            'error': str(e)
        }

@celery.task(bind=True, name='initialize_music_database')
def initialize_music_database(self, max_videos=50):
    """
    Initialize the music database with trending videos
    """
    try:
        self.update_state(
            state='PROGRESS',
            meta={'current': 1, 'total': 3, 'percent': 33, 'status': 'Initializing services...'}
        )
        
        # Initialize recommendation service
        recommendation_service = RecommendationService()
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 2, 'total': 3, 'percent': 66, 'status': f'Processing {max_videos} trending videos...'}
        )
        
        # Initialize database
        result = recommendation_service.initialize_music_database(max_videos)
        
        self.update_state(
            state='PROGRESS',
            meta={'current': 3, 'total': 3, 'percent': 100, 'status': 'Database initialization complete!'}
        )
        
        return {
            'status': 'Completed',
            'result': result,
            'message': f"Processed {result.get('processed', 0)} videos, failed {result.get('failed', 0)}"
        }
        
    except Exception as e:
        logger.error(f"Error in initialize_music_database task: {e}")
        return {
            'status': 'Failed',
            'error': str(e)
        }