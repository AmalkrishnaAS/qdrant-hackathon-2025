import time
import json
import logging
from flask import Response, request
from flask_restx import Namespace, Resource, fields, reqparse
from celery.result import AsyncResult
from app.tasks import create_task
from app.extensions import celery
from app.services.music_vectorization_service import MusicVectorizationService
from config.config import Config
from flask_cors import cross_origin

logger = logging.getLogger(__name__)

# Create namespace
api = Namespace('tasks', description='Long-running task operations')

# Request/Response Models
task_request_model = api.model('TaskRequest', {
    'video_id': fields.String(required=True, description='YouTube video ID to process')
})

search_request_model = api.model('SearchRequest', {
    'query': fields.String(required=True, description='Text query for semantic search'),
    'limit': fields.Integer(required=False, default=5, description='Number of results to return (max: 20)')
})

task_status_model = api.model('TaskStatus', {
    'task_id': fields.String(required=True, description='The ID of the task'),
    'status': fields.String(required=True, description='Current status (PENDING, STARTED, PROCESSING, SUCCESS, FAILURE)'),
    'result': fields.Raw(description='Task result or error details'),
    'progress': fields.Float(description='Progress percentage (0-100)', required=False),
    'current_step': fields.Integer(description='Current processing step', required=False),
    'total_steps': fields.Integer(description='Total processing steps', required=False),
    'start_time': fields.String(description='Task start timestamp'),
    'end_time': fields.String(description='Task completion timestamp', required=False),
    'duration_seconds': fields.Float(description='Task duration in seconds', required=False),
    'collection': fields.String(description='Qdrant collection used', required=False),
    'vector_dim': fields.Integer(description='Dimension of the stored vector', required=False)
})

search_result_model = api.model('SearchResult', {
    'id': fields.String(description='Result ID'),
    'score': fields.Float(description='Similarity score'),
    'payload': fields.Raw(description='Stored metadata')
})

# --- API Endpoints ---

@api.route('/')
class TaskList(Resource):
    @api.doc('create_task')
    @api.expect(task_request_model)
    @api.marshal_with(task_status_model, code=202)

    @cross_origin(supports_credentials=True,headers=['Content-Type'])
    def post(self):
        """
        Start processing a YouTube video: download audio, extract features, and store in Qdrant
        """
        data = request.json
        video_id = data.get('video_id')
        
        if not video_id:
            return {'message': 'video_id is required'}, 400
            
        try:
            # Start the task with video_id
            task = create_task.apply_async(args=[video_id])
            
            # Store task reference in Redis
            celery.backend.client.rpush('task_list', task.id)
            
            return {
                'task_id': task.id, 
                'status': task.status,
                'video_id': video_id,
                'collection': Config.QDRANT_COLLECTION_NAME
            }, 202
            
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return {'message': f'Failed to create task: {str(e)}'}, 500

    @api.doc('list_tasks')
    @api.marshal_list_with(task_status_model)
    def get(self):
        """
        List all created tasks with their current status
        """
        task_ids = celery.backend.client.lrange('task_list', 0, -1)
        tasks = []
        for task_id_bytes in task_ids:
            task_id = task_id_bytes.decode('utf-8')
            result = AsyncResult(task_id, app=celery)
            
            # Initialize task info with basic fields
            task_info = {
                'task_id': task_id,
                'status': result.state,
                'result': None,
                'progress': None,
                'current_step': None,
                'total_steps': None,
                'start_time': None,
                'end_time': None,
                'duration_seconds': None,
                'collection': None,
                'vector_dim': None
            }
            
            # Add detailed info based on task state
            if result.info and isinstance(result.info, dict):
                if result.state == 'SUCCESS':
                    task_info.update({
                        'status': result.info.get('status', result.state),
                        'result': result.info,
                        'progress': 100.0,
                        'start_time': result.info.get('start_time'),
                        'end_time': result.info.get('end_time'),
                        'duration_seconds': result.info.get('duration_seconds'),
                        'collection': result.info.get('collection'),
                        'vector_dim': result.info.get('vector_dim')
                    })
                else:
                    task_info.update({
                        'result': result.info,
                        'progress': result.info.get('progress'),
                        'current_step': result.info.get('current_step'),
                        'total_steps': result.info.get('total_steps'),
                        'start_time': result.info.get('start_time'),
                        'collection': result.info.get('collection'),
                        'vector_dim': result.info.get('vector_dim')
                    })
            
            tasks.append(task_info)
            
        return tasks


@api.route('/<string:task_id>')
class TaskStatus(Resource):
    @api.doc('get_task_status')
    @api.marshal_with(task_status_model)
    def get(self, task_id):
        """
        Get the status of a specific task
        """
        result = AsyncResult(task_id, app=celery)
        
        # Initialize response with basic task info
        response = {
            'task_id': task_id,
            'status': result.state,
            'result': None,
            'progress': None,
            'current_step': None,
            'total_steps': None,
            'start_time': None,
            'end_time': None,
            'duration_seconds': None,
            'collection': None,
            'vector_dim': None
        }
        
        # If we have result info, update the response with it
        if result.info and isinstance(result.info, dict):
            # For SUCCESS state, the result is in result.info
            if result.state == 'SUCCESS':
                response.update({
                    'status': result.info.get('status', result.state),
                    'result': result.info,
                    'progress': 100.0,
                    'start_time': result.info.get('start_time'),
                    'end_time': result.info.get('end_time'),
                    'duration_seconds': result.info.get('duration_seconds'),
                    'collection': result.info.get('collection'),
                    'vector_dim': result.info.get('vector_dim')
                })
            # For other states, update available fields
            else:
                response.update({
                    'result': result.info,
                    'progress': result.info.get('progress'),
                    'current_step': result.info.get('current_step'),
                    'total_steps': result.info.get('total_steps'),
                    'start_time': result.info.get('start_time'),
                    'collection': result.info.get('collection'),
                    'vector_dim': result.info.get('vector_dim')
                })
        # For task meta during processing
        elif result.state == 'PROGRESS' and result.info and isinstance(result.info, dict):
            response.update({
                'status': result.info.get('status', result.state),
                'message': result.info.get('message'),
                'progress': result.info.get('progress'),
                'current_step': result.info.get('current_step'),
                'total_steps': result.info.get('total_steps'),
                'start_time': result.info.get('start_time')
            })
            
        return response

@api.route('/events/list')
class TaskListEvents(Resource):
    @api.doc('get_task_list_events_sse')
    def get(self):
        """
        Get real-time updates for all tasks using Server-Sent Events (SSE)
        """
        def event_stream():
            last_tasks = {}
            
            while True:
                # Get current task list
                task_ids_bytes = celery.backend.client.lrange('task_list', 0, -1)
                current_tasks = {}
                
                # Get current state of all tasks
                for task_id_bytes in task_ids_bytes:
                    task_id = task_id_bytes.decode('utf-8')
                    result = AsyncResult(task_id, app=celery)
                    
                    # Build task info
                    task_info = {
                        'task_id': task_id,
                        'status': result.state,
                    }
                    
                    # Add additional info if available
                    if result.info and isinstance(result.info, dict):
                        task_info.update(result.info)
                    elif result.state != 'PENDING':
                        task_info['result'] = result.info
                    
                    current_tasks[task_id] = task_info
                
                # Check if there are any changes
                if current_tasks != last_tasks:
                    # Send updated task list
                    data = {
                        'event': 'task_list_update',
                        'data': list(current_tasks.values())
                    }
                    yield f"data: {json.dumps(data)}\n\n"
                    last_tasks = current_tasks
                
                # Wait before next poll
                time.sleep(1)
        
        # Return the SSE response
        return Response(
            event_stream(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'  # Disable buffering for nginx
            }
        )

@api.route('/<string:task_id>/events')
class TaskEvents(Resource):
    @api.doc('get_task_events_sse')
    def get(self, task_id):
        """
        Get real-time task status updates using Server-Sent Events (SSE)
        """
        def event_stream():
            last_state = None
            
            while True:
                try:
                    result = AsyncResult(task_id, app=celery)
                    
                    # Build task info
                    task_info = {
                        'task_id': task_id,
                        'status': result.state,
                    }
                    
                    # Add additional info if available
                    if result.info and isinstance(result.info, dict):
                        task_info.update(result.info)
                    elif result.state != 'PENDING':
                        task_info['result'] = result.info
                    
                    # Only send update if something changed
                    if task_info != last_state:
                        data = {
                            'event': 'task_update',
                            'data': task_info
                        }
                        yield f"data: {json.dumps(data)}\n\n"
                        last_state = task_info
                    
                    # Stop if task is complete
                    if result.state in ('SUCCESS', 'FAILURE'):
                        # Add timing information for completed tasks
                        if result.state == 'SUCCESS' and isinstance(result.info, dict):
                            if 'start_time' in result.info and 'end_time' in result.info:
                                try:
                                    start = time.mktime(time.strptime(result.info['start_time'], '%Y-%m-%d %H:%M:%S'))
                                    end = time.mktime(time.strptime(result.info['end_time'], '%Y-%m-%d %H:%M:%S'))
                                    task_info['duration_seconds'] = end - start
                                except (ValueError, TypeError) as e:
                                    logger.warning(f"Error calculating duration: {e}")
                        
                        # Send final state
                        final_data = {
                            'event': 'task_complete',
                            'data': task_info
                        }
                        yield f"data: {json.dumps(final_data)}\n\n"
                        break
                        
                except Exception as e:
                    logger.error(f"Error in SSE stream for task {task_id}: {str(e)}")
                    yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
                    break
                    
                # Wait before next poll
                time.sleep(1)
        
        # Return the SSE response
        return Response(
            event_stream(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no'
            }
        )

@api.route('/search')
class VectorSearch(Resource):
    @api.doc('search_similar_vectors')
    @api.expect(search_request_model)
    @api.marshal_list_with(search_result_model)
    def post(self):
        """
        Search for similar vectors using a text query
        """
        data = request.json
        query = data.get('query')
        collection_name = data.get('collection', 'youtube_audio_vectors')
        limit = min(int(data.get('limit', 5)), 20)  # Cap at 20 results
        
        if not query:
            return {'message': 'query is required'}, 400
            
        try:
            # Initialize vectorization service
            vector_service = MusicVectorizationService()
            
            # Get text embedding
            query_vector = vector_service.extract_text_features(query)
            
            # Search in Qdrant
            search_result = vector_service.qdrant_client.search(
                collection_name=Config.QDRANT_COLLECTION_NAME,
                query_vector=query_vector,
                limit=min(limit, 20)  # Ensure limit doesn't exceed 20
            )
            
            # Format results
            results = []
            for hit in search_result:
                results.append({
                    'id': str(hit.id),
                    'score': hit.score,
                    'payload': hit.payload or {}
                })
                
            return results
            
        except Exception as e:
            logger.error(f"Vector search error: {str(e)}")
            return {'message': f'Search failed: {str(e)}'}, 500