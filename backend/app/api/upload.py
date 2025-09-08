from flask_restx import Namespace, Resource, fields
from flask import current_app, request
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from app.models.schemas import UploadResponse, ErrorResponse, ProcessRequest, ProcessResponse
import os
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Create namespace
api = Namespace('upload', description='File upload operations')

# Define models for Swagger documentation
upload_response_model = api.model('UploadResponse', {
    'success': fields.Boolean(default=True),
    'data': fields.Raw(description='Upload information'),
    'message': fields.String(required=False)
})

process_request_model = api.model('ProcessRequest', {
    'video_file': fields.String(required=True, description='Path to uploaded video file'),
    'selected_track_id': fields.String(required=True, description='ID of selected audio track'),
    'start_time': fields.Float(default=0.0, description='Start time for audio crop in seconds'),
    'end_time': fields.Float(required=False, description='End time for audio crop in seconds'),
    'output_format': fields.String(default='mp4', description='Output file format')
})

process_response_model = api.model('ProcessResponse', {
    'success': fields.Boolean(default=True),
    'data': fields.Raw(description='Processing result information'),
    'message': fields.String(required=False),
    'processing_id': fields.String(required=False)
})

error_model = api.model('Error', {
    'success': fields.Boolean(default=False),
    'message': fields.String(required=True),
    'error_code': fields.String(required=False)
})

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def get_file_type(filename):
    """Determine file type based on extension"""
    if '.' not in filename:
        return 'unknown'
    
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in ['mp4', 'avi', 'mov', 'mkv', 'webm']:
        return 'video'
    elif ext in ['mp3', 'wav', 'flac', 'aac', 'm4a']:
        return 'audio'
    elif ext in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']:
        return 'image'
    else:
        return 'unknown'

@api.route('/')
class FileUpload(Resource):
    @api.doc('upload_file')
    @api.marshal_with(upload_response_model)
    @api.expect(api.parser()
                .add_argument('files', location='files', type='FileStorage', 
                            action='append', required=True, 
                            help='Files to upload (video, audio, or image)'))
    def post(self):
        """
        Upload files for processing
        Accepts video, audio, or image files and stores them for processing
        """
        try:
            if 'files' not in request.files:
                raise BadRequest("No files provided")
            
            files = request.files.getlist('files')
            if not files or files[0].filename == '':
                raise BadRequest("No files selected")
            
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(current_app.root_path, '..', current_app.config['UPLOAD_FOLDER'])
            os.makedirs(upload_dir, exist_ok=True)
            
            uploaded_files = []
            
            for file in files:
                if file and allowed_file(file.filename):
                    # Generate unique filename
                    original_filename = file.filename
                    file_extension = original_filename.rsplit('.', 1)[1].lower()
                    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
                    secure_name = secure_filename(unique_filename)
                    
                    # Save file
                    file_path = os.path.join(upload_dir, secure_name)
                    file.save(file_path)
                    
                    # Get file info
                    file_size = os.path.getsize(file_path)
                    file_type = get_file_type(original_filename)
                    
                    upload_info = {
                        "filename": secure_name,
                        "original_filename": original_filename,
                        "file_size": file_size,
                        "file_type": file_type,
                        "upload_path": file_path,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    uploaded_files.append(upload_info)
                    logger.info(f"Uploaded file: {original_filename} as {secure_name}")
                
                else:
                    logger.warning(f"Rejected file: {file.filename if file else 'None'} (not allowed)")
            
            if not uploaded_files:
                raise BadRequest("No valid files were uploaded")
            
            response = UploadResponse(
                data=uploaded_files,
                message=f"Successfully uploaded {len(uploaded_files)} file(s)"
            )
            
            return response.dict(), 200
            
        except RequestEntityTooLarge:
            error_response = ErrorResponse(
                message="File too large. Maximum size allowed is 100MB",
                error_code="FILE_TOO_LARGE"
            )
            return error_response.dict(), 413
            
        except BadRequest as e:
            error_response = ErrorResponse(
                message=str(e.description),
                error_code="BAD_REQUEST"
            )
            return error_response.dict(), 400
            
        except Exception as e:
            logger.error(f"Error uploading files: {e}")
            error_response = ErrorResponse(
                message="Failed to upload files",
                error_code="UPLOAD_ERROR"
            )
            return error_response.dict(), 500

@api.route('/process')
class ProcessFiles(Resource):
    @api.doc('process_files')
    @api.expect(process_request_model)
    @api.marshal_with(process_response_model)
    def post(self):
        """
        Process uploaded video with selected audio track
        Combines uploaded video with selected audio track and applies any requested edits
        """
        try:
            data = request.get_json()
            if not data:
                raise BadRequest("No processing data provided")
            
            # Validate request
            req = ProcessRequest(**data)
            
            # Check if video file exists
            upload_dir = os.path.join(current_app.root_path, '..', current_app.config['UPLOAD_FOLDER'])
            video_path = os.path.join(upload_dir, req.video_file)
            
            if not os.path.exists(video_path):
                raise BadRequest(f"Video file not found: {req.video_file}")
            
            # Generate processing ID
            processing_id = uuid.uuid4().hex
            
            # Create output directory
            output_dir = os.path.join(current_app.root_path, '..', 'static', 'processed')
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename
            output_filename = f"{processing_id}.{req.output_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            # TODO: Implement actual video processing with FFmpeg/MoviePy
            # For now, we'll simulate processing and copy the original file
            logger.info(f"Processing video: {req.video_file} with track: {req.selected_track_id}")
            logger.info(f"Audio crop: {req.start_time}s to {req.end_time or 'end'}")
            
            # Simulate processing delay (remove in production)
            import time
            time.sleep(1)
            
            # For demo purposes, just copy the original file
            import shutil
            shutil.copy2(video_path, output_path)
            
            # Generate download URL
            download_url = f"/api/songs/{req.selected_track_id}/download"
            
            response_data = {
                "processing_id": processing_id,
                "output_file": output_filename,
                "output_path": output_path,
                "download_url": download_url,
                "video_file": req.video_file,
                "selected_track_id": req.selected_track_id,
                "start_time": req.start_time,
                "end_time": req.end_time,
                "output_format": req.output_format,
                "processed_at": datetime.now().isoformat()
            }
            
            response = ProcessResponse(
                data=response_data,
                message="Video processing completed successfully",
                processing_id=processing_id
            )
            
            return response.dict(), 200
            
        except ValueError as e:
            logger.error(f"Validation error in processing: {e}")
            error_response = ErrorResponse(
                message=f"Invalid request data: {str(e)}",
                error_code="VALIDATION_ERROR"
            )
            return error_response.dict(), 400
            
        except BadRequest as e:
            error_response = ErrorResponse(
                message=str(e.description),
                error_code="BAD_REQUEST"
            )
            return error_response.dict(), 400
            
        except Exception as e:
            logger.error(f"Error processing files: {e}")
            error_response = ErrorResponse(
                message="Failed to process files",
                error_code="PROCESSING_ERROR"
            )
            return error_response.dict(), 500

@api.route('/status/<string:processing_id>')
class ProcessingStatus(Resource):
    @api.doc('get_processing_status')
    def get(self, processing_id):
        """
        Get processing status
        Returns the current status of a file processing job
        """
        try:
            # Check if processed file exists
            output_dir = os.path.join(current_app.root_path, '..', 'static', 'processed')
            possible_files = [
                f"{processing_id}.mp4",
                f"{processing_id}.avi",
                f"{processing_id}.mov"
            ]
            
            processed_file = None
            for filename in possible_files:
                file_path = os.path.join(output_dir, filename)
                if os.path.exists(file_path):
                    processed_file = filename
                    break
            
            if processed_file:
                return {
                    "success": True,
                    "status": "completed",
                    "processing_id": processing_id,
                    "output_file": processed_file,
                    "download_ready": True,
                    "message": "Processing completed successfully"
                }, 200
            else:
                return {
                    "success": True,
                    "status": "processing",
                    "processing_id": processing_id,
                    "download_ready": False,
                    "message": "File is still being processed"
                }, 200
                
        except Exception as e:
            logger.error(f"Error checking processing status: {e}")
            error_response = ErrorResponse(
                message="Failed to check processing status",
                error_code="STATUS_ERROR"
            )
            return error_response.dict(), 500

