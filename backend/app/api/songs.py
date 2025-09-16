import logging
import os
from flask_restx import Namespace, Resource, fields, reqparse
from flask import current_app, request, send_file, abort
from werkzeug.exceptions import BadRequest, NotFound
from app.models.schemas import Song, SongResponse, RecommendationRequest, RecommendationResponse, ErrorResponse
from app.services.qdrant_service import QdrantService
from app.services.data_service import DataService

logger = logging.getLogger(__name__)

try:
    from app.services.recommendation_service import RecommendationService
    AI_SERVICES_AVAILABLE = True
except ImportError as e:
    logger.warning(f"AI services not available: {e}")
    RecommendationService = None
    AI_SERVICES_AVAILABLE = False

# Create namespace
api = Namespace('songs', description='Song operations')

# Define models for Swagger documentation
thumbnail_model = api.model('Thumbnail', {
    'url': fields.String(required=True),
    'width': fields.Integer(required=True),
    'height': fields.Integer(required=True)
})

thumbnails_model = api.model('Thumbnails', {
    'default': fields.Nested(thumbnail_model, required=True),
    'medium': fields.Nested(thumbnail_model, required=True),
    'high': fields.Nested(thumbnail_model, required=True)
})

song_model = api.model('Song', {
    'id': fields.String(required=True),
    'title': fields.String(required=True),
    'artists': fields.List(fields.String, required=True),
    'album': fields.String(required=True),
    'duration': fields.String(required=True),
    'thumbnails': fields.Nested(thumbnails_model, required=True),
    'videoId': fields.String(required=True),
    'isExplicit': fields.Boolean(default=False),
    'category': fields.String(required=True),
    'description': fields.String(required=True),
    'audioUrl': fields.String(required=False)
})

song_response_model = api.model('SongResponse', {
    'success': fields.Boolean(default=True),
    'data': fields.List(fields.Nested(song_model)),
    'message': fields.String(required=False),
    'total': fields.Integer(required=False)
})

recommendation_request_model = api.model('RecommendationRequest', {
    'uploaded_files': fields.List(fields.String, required=False, default=[]),
    'query': fields.String(required=False),
    'limit': fields.Integer(default=10, min=1, max=50),
    'include_metadata': fields.Boolean(default=True)
})

error_model = api.model('Error', {
    'success': fields.Boolean(default=False),
    'message': fields.String(required=True),
    'error_code': fields.String(required=False)
})

# Global services (will be initialized per request)
def get_services():
    """Get initialized services"""
    qdrant_service = QdrantService(
        host=current_app.config['QDRANT_HOST'],
        port=current_app.config['QDRANT_PORT'],
        api_key=current_app.config.get('QDRANT_API_KEY')
    )
    data_service = DataService(qdrant_service)
    
    recommendation_service = None
    if AI_SERVICES_AVAILABLE and RecommendationService:
        try:
            recommendation_service = RecommendationService(
                qdrant_host=current_app.config['QDRANT_HOST'],
                qdrant_port=current_app.config['QDRANT_PORT'],
                qdrant_api_key=current_app.config.get('QDRANT_API_KEY')
            )
        except Exception as e:
            logger.warning(f"Failed to initialize recommendation service: {e}")
            recommendation_service = None
    
    return qdrant_service, data_service, recommendation_service

@api.route('/trending')
class TrendingSongs(Resource):
    @api.doc('get_trending_songs')
    @api.marshal_with(song_response_model)
    @api.param('limit', 'Number of songs to return', type='integer', default=10)
    def get(self):
        """
        Get trending songs
        Returns a list of currently trending songs
        """
        try:
            limit = request.args.get('limit', 10, type=int)
            limit = min(max(limit, 1), 50)  # Ensure limit is between 1 and 50
            
            qdrant_service, data_service, recommendation_service = get_services()
            
            if recommendation_service:
                try:
                    # Try to get trending recommendations from the music database
                    songs = recommendation_service.get_trending_recommendations(limit=limit)
                    
                    if not songs:
                        # Fallback to data service if recommendation service fails
                        logger.info("No trending results from recommendation service, using fallback data")
                        data_service.initialize_data()
                        songs = data_service.get_all_songs()[:limit]
                        
                except Exception as e:
                    logger.warning(f"Error getting trending recommendations: {e}")
                    # Fallback to data service
                    data_service.initialize_data()
                    songs = data_service.get_all_songs()[:limit]
            else:
                # No AI services available, use fallback data
                logger.info("AI services not available, using fallback data")
                data_service.initialize_data()
                songs = data_service.get_all_songs()[:limit]
            
            response = SongResponse(
                data=songs,
                total=len(songs),
                message="Trending songs retrieved successfully"
            )
            
            return response.dict(), 200
            
        except Exception as e:
            logger.error(f"Error getting trending songs: {e}")
            error_response = ErrorResponse(
                message="Failed to retrieve trending songs",
                error_code="TRENDING_ERROR"
            )
            return error_response.dict(), 500

@api.route('/recommendations')
class Recommendations(Resource):
    @api.doc('get_recommendations')
    @api.expect(recommendation_request_model)
    @api.marshal_with(song_response_model)
    def post(self):
        """
        Get song recommendations
        Returns personalized song recommendations based on uploaded content or query
        """
        try:
            data = request.get_json()
            if not data:
                data = {}
            
            # Validate request
            req = RecommendationRequest(**data)
            
            qdrant_service, data_service, recommendation_service = get_services()
            
            # Generate recommendations using the new recommendation service
            if recommendation_service:
                try:
                    if req.query:
                        # Use text query for recommendations
                        logger.info(f"Getting recommendations for query: {req.query}")
                        songs = recommendation_service.recommend_by_text_query(
                            query=req.query, 
                            limit=req.limit
                        )
                    elif req.uploaded_files:
                        # For now, analyze the first uploaded file if it's a video
                        # In a real implementation, you'd handle multiple files
                        logger.info(f"Getting recommendations for {len(req.uploaded_files)} uploaded files")
                        
                        # For this demo, we'll use a generic music query
                        # In production, you'd analyze the uploaded video files
                        songs = recommendation_service.recommend_by_text_query(
                            query="energetic upbeat music for videos", 
                            limit=req.limit
                        )
                    else:
                        # Default recommendations
                        logger.info("Getting default trending recommendations")
                        songs = recommendation_service.get_trending_recommendations(limit=req.limit)
                    
                    if not songs:
                        # Fallback to data service
                        logger.info("No recommendations from service, using fallback data")
                        data_service.initialize_data()
                        songs = data_service.get_all_songs()[:req.limit]
                        
                except Exception as e:
                    logger.warning(f"Error getting recommendations from service: {e}")
                    # Fallback to data service
                    data_service.initialize_data()
                    songs = data_service.get_all_songs()[:req.limit]
            else:
                # No AI services available, use fallback data
                logger.info("AI services not available, using fallback data")
                data_service.initialize_data()
                songs = data_service.get_all_songs()[:req.limit]
            
            response = RecommendationResponse(
                data=songs,
                message="Recommendations retrieved successfully",
                query_info={
                    "query": req.query,
                    "uploaded_files_count": len(req.uploaded_files) if req.uploaded_files else 0,
                    "results_count": len(songs)
                }
            )
            
            return response.dict(), 200
            
        except ValueError as e:
            logger.error(f"Validation error in recommendations: {e}")
            error_response = ErrorResponse(
                message=f"Invalid request data: {str(e)}",
                error_code="VALIDATION_ERROR"
            )
            return error_response.dict(), 400
            
        except Exception as e:
            logger.error(f"Error getting recommendations: {e}")
            error_response = ErrorResponse(
                message="Failed to get recommendations",
                error_code="RECOMMENDATION_ERROR"
            )
            return error_response.dict(), 500

@api.route('/')
class SongsList(Resource):
    @api.doc('list_songs')
    @api.marshal_with(song_response_model)
    @api.param('limit', 'Number of songs to return', type='integer', default=20)
    @api.param('category', 'Filter by category', type='string')
    def get(self):
        """
        List all songs
        Returns a paginated list of all available songs
        """
        try:
            limit = request.args.get('limit', 20, type=int)
            category = request.args.get('category')
            limit = min(max(limit, 1), 100)  # Ensure limit is between 1 and 100
            
            qdrant_service, data_service, recommendation_service = get_services()
            
            # Initialize data if needed
            data_service.initialize_data()
            
            if category:
                # Filter by category using Qdrant
                results = qdrant_service.search_by_categories([category], limit=limit)
                songs = []
                for result in results:
                    song_id = result['id']
                    song = data_service.get_song_by_id(song_id)
                    if song:
                        songs.append(song)
            else:
                # Return all songs (or limited set)
                songs = data_service.get_all_songs()[:limit]
            
            response = SongResponse(
                data=songs,
                total=len(songs),
                message=f"Songs retrieved successfully{' for category: ' + category if category else ''}"
            )
            
            return response.dict(), 200
            
        except Exception as e:
            logger.error(f"Error listing songs: {e}")
            error_response = ErrorResponse(
                message="Failed to retrieve songs",
                error_code="SONGS_LIST_ERROR"
            )
            return error_response.dict(), 500

@api.route('/<string:song_id>/download')
class DownloadSong(Resource):
    @api.doc('download_song')
    def get(self, song_id):
        """
        Download a processed song/video file
        Returns the processed audio/video file for download
        """
        try:
            qdrant_service, data_service, recommendation_service = get_services()
            
            # Get song info
            song = data_service.get_song_by_id(song_id)
            if not song:
                raise NotFound("Song not found")
            
            # In a real implementation, you'd return the processed file
            # For now, we'll return a placeholder response
            logger.info(f"Download requested for song: {song.title}")
            
            # Check if processed file exists
            processed_file_path = os.path.join(
                current_app.root_path, '..', 'static', 'processed', f"{song_id}.mp4"
            )
            
            if os.path.exists(processed_file_path):
                return send_file(
                    processed_file_path,
                    as_attachment=True,
                    download_name=f"{song.title}.mp4",
                    mimetype='video/mp4'
                )
            else:
                # Return info about where the file would be
                return {
                    "success": False,
                    "message": "Processed file not ready yet. Please process the video first.",
                    "song": {
                        "id": song.id,
                        "title": song.title,
                        "videoId": song.videoId
                    }
                }, 404
                
        except NotFound:
            error_response = ErrorResponse(
                message=f"Song with ID {song_id} not found",
                error_code="SONG_NOT_FOUND"
            )
            return error_response.dict(), 404
            
        except Exception as e:
            logger.error(f"Error downloading song {song_id}: {e}")
            error_response = ErrorResponse(
                message="Failed to download song",
                error_code="DOWNLOAD_ERROR"
            )
            return error_response.dict(), 500

