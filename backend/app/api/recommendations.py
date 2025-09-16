from flask_restx import Namespace, Resource, fields, reqparse
from flask import current_app, request
from werkzeug.exceptions import BadRequest, NotFound
from app.models.schemas import ErrorResponse
from app.services.recommendation_service import RecommendationService
from app.tasks import analyze_video_and_recommend, initialize_music_database
import logging
import os
import tempfile
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# Create namespace
api = Namespace('recommendations', description='AI-powered music recommendation operations')

# Define models for Swagger documentation
video_analysis_request = api.model('VideoAnalysisRequest', {
    'limit': fields.Integer(default=10, min=1, max=50, description='Number of recommendations to return')
})

video_analysis_response = api.model('VideoAnalysisResponse', {
    'success': fields.Boolean(default=True),
    'task_id': fields.String(required=True, description='Task ID for tracking progress'),
    'message': fields.String(required=False)
})

database_init_request = api.model('DatabaseInitRequest', {
    'max_videos': fields.Integer(default=50, min=10, max=200, description='Number of trending videos to process')
})

database_init_response = api.model('DatabaseInitResponse', {
    'success': fields.Boolean(default=True),
    'task_id': fields.String(required=True, description='Task ID for tracking progress'),
    'message': fields.String(required=False)
})

database_stats_response = api.model('DatabaseStatsResponse', {
    'success': fields.Boolean(default=True),
    'data': fields.Raw(required=True, description='Database statistics'),
    'message': fields.String(required=False)
})

error_model = api.model('Error', {
    'success': fields.Boolean(default=False),
    'message': fields.String(required=True),
    'error_code': fields.String(required=False)
})

def get_recommendation_service():
    """Get initialized recommendation service"""
    return RecommendationService(
        qdrant_host=current_app.config['QDRANT_HOST'],
        qdrant_port=current_app.config['QDRANT_PORT'],
        qdrant_api_key=current_app.config.get('QDRANT_API_KEY')
    )

@api.route('/analyze-video')
class VideoAnalysis(Resource):
    @api.doc('analyze_video_for_recommendations')
    @api.expect(video_analysis_request)
    @api.marshal_with(video_analysis_response)
    def post(self):
        """
        Analyze uploaded video and get music recommendations
        Upload a video file and get AI-powered music recommendations based on the video content
        """
        try:
            # Check if file was uploaded
            if 'video' not in request.files:
                raise BadRequest("No video file uploaded")
            
            file = request.files['video']
            if file.filename == '':
                raise BadRequest("No video file selected")
            
            # Get request parameters
            data = request.form.to_dict()
            limit = int(data.get('limit', 10))
            limit = min(max(limit, 1), 50)  # Ensure limit is between 1 and 50
            
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            temp_dir = tempfile.mkdtemp()
            temp_path = os.path.join(temp_dir, filename)
            file.save(temp_path)
            
            logger.info(f"Video uploaded: {filename}, starting analysis task")
            
            # Start background task for video analysis
            task = analyze_video_and_recommend.delay(temp_path, limit)
            
            return {
                'success': True,
                'task_id': task.id,
                'message': f'Video analysis started for {filename}. Use the task ID to check progress.'
            }, 202
            
        except BadRequest as e:
            error_response = ErrorResponse(
                message=str(e),
                error_code="BAD_REQUEST"
            )
            return error_response.dict(), 400
            
        except Exception as e:
            logger.error(f"Error starting video analysis: {e}")
            error_response = ErrorResponse(
                message="Failed to start video analysis",
                error_code="ANALYSIS_ERROR"
            )
            return error_response.dict(), 500

@api.route('/text-recommendations')
class TextRecommendations(Resource):
    @api.doc('get_text_recommendations')
    def post(self):
        """
        Get music recommendations based on text description
        Provide a text description and get matching music recommendations
        """
        try:
            data = request.get_json()
            if not data or 'query' not in data:
                raise BadRequest("Query text is required")
            
            query = data['query']
            limit = data.get('limit', 10)
            limit = min(max(limit, 1), 50)
            
            logger.info(f"Getting text-based recommendations for: {query}")
            
            # Get recommendation service
            recommendation_service = get_recommendation_service()
            
            # Get recommendations
            songs = recommendation_service.recommend_by_text_query(query, limit=limit)
            
            return {
                'success': True,
                'data': [song.dict() for song in songs],
                'total': len(songs),
                'message': f'Found {len(songs)} recommendations for your query'
            }, 200
            
        except BadRequest as e:
            error_response = ErrorResponse(
                message=str(e),
                error_code="BAD_REQUEST"
            )
            return error_response.dict(), 400
            
        except Exception as e:
            logger.error(f"Error getting text recommendations: {e}")
            error_response = ErrorResponse(
                message="Failed to get recommendations",
                error_code="RECOMMENDATION_ERROR"
            )
            return error_response.dict(), 500

@api.route('/initialize-database')
class InitializeDatabase(Resource):
    @api.doc('initialize_music_database')
    @api.expect(database_init_request)
    @api.marshal_with(database_init_response)
    def post(self):
        """
        Initialize music database with trending videos
        Download and process trending music videos to populate the recommendation database
        """
        try:
            data = request.get_json()
            if not data:
                data = {}
            
            max_videos = data.get('max_videos', 50)
            max_videos = min(max(max_videos, 10), 200)  # Ensure between 10 and 200
            
            logger.info(f"Starting database initialization with {max_videos} videos")
            
            # Start background task for database initialization
            task = initialize_music_database.delay(max_videos)
            
            return {
                'success': True,
                'task_id': task.id,
                'message': f'Database initialization started. Processing {max_videos} trending videos.'
            }, 202
            
        except Exception as e:
            logger.error(f"Error starting database initialization: {e}")
            error_response = ErrorResponse(
                message="Failed to start database initialization",
                error_code="INIT_ERROR"
            )
            return error_response.dict(), 500

@api.route('/database-stats')
class DatabaseStats(Resource):
    @api.doc('get_database_stats')
    @api.marshal_with(database_stats_response)
    def get(self):
        """
        Get music database statistics
        Returns information about the current state of the music recommendation database
        """
        try:
            logger.info("Getting database statistics")
            
            # Get recommendation service
            recommendation_service = get_recommendation_service()
            
            # Get database stats
            stats = recommendation_service.get_database_stats()
            
            return {
                'success': True,
                'data': stats,
                'message': 'Database statistics retrieved successfully'
            }, 200
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            error_response = ErrorResponse(
                message="Failed to get database statistics",
                error_code="STATS_ERROR"
            )
            return error_response.dict(), 500
