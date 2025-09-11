import time
import json
from flask import Response, request
from flask_restx import Namespace, Resource, fields
from celery.result import AsyncResult
from app.tasks import create_task # Import the task we created
from app.extensions import celery # <- NEW

# Create namespace
api = Namespace('tasks', description='Long-running task operations')

# Define models for Swagger documentation
task_request_model = api.model('TaskRequest', {
    'video_id': fields.String(required=True, description='The ID of the video to process')
})

task_status_model = api.model('TaskStatus', {
    'task_id': fields.String(required=True, description='The ID of the task'),
    'status': fields.String(required=True, description='The current status of the task (e.g., PENDING, SUCCESS, FAILURE)'),
    'result': fields.Raw(description='The result of the task, if completed')
})

# --- API Endpoints ---

@api.route('/')
class TaskList(Resource):
    @api.doc('create_task')
    @api.expect(task_request_model)
    @api.marshal_with(task_status_model, code=202)
    def post(self):
        """
        Create (start) a new long-running task
        """
        video_id = request.json.get('video_id')
        if not video_id:
            return {'message': 'video_id is required'}, 400

        # Use .apply_async() to start the task
        task = create_task.apply_async(args=[video_id])
        
        # Store a reference to the task_id in Redis for the list endpoint
        # We use a simple Redis list as a task log
        celery.backend.client.rpush('task_list', task.id)

        return {'task_id': task.id, 'status': task.status}, 202

    @api.doc('list_tasks')
    @api.marshal_list_with(task_status_model)
    def get(self):
        """
        List all created tasks
        """
        task_ids = celery.backend.client.lrange('task_list', 0, -1)
        tasks = []
        for task_id_bytes in task_ids:
            task_id = task_id_bytes.decode('utf-8')
            result = AsyncResult(task_id, app=celery)
            tasks.append({
                'task_id': task_id,
                'status': result.state,
                'result': result.info if result.state != 'PENDING' else None
            })
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
        response = {
            'task_id': task_id,
            'status': result.state,
            'result': result.info, # .info contains the result or error info
        }
        return response

@api.route('/<string:task_id>/events')
class TaskEvents(Resource):
    @api.doc('get_task_events_sse')
    def get(self, task_id):
        """
        Get real-time task status updates using Server-Sent Events (SSE)
        """
        def event_stream():
            result = AsyncResult(task_id, app=celery)
            while result.state not in ('SUCCESS', 'FAILURE'):
                result = AsyncResult(task_id, app=celery) # Re-fetch status
                data = {
                    'task_id': task_id,
                    'status': result.state,
                    'meta': result.info if isinstance(result.info, dict) else {}
                }
                # SSE format: "data: <json_string>\n\n"
                yield f"data: {json.dumps(data)}\n\n"
                time.sleep(1)  # Poll every second

            # Send final state
            final_data = {
                'task_id': task_id,
                'status': result.state,
                'result': result.info
            }
            yield f"data: {json.dumps(final_data)}\n\n"

        return Response(event_stream(), mimetype='text/event-stream')