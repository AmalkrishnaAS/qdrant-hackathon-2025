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
                logger.error("No 'files' key in request.files")
                raise BadRequest("No files provided")
            
            files = request.files.getlist('files')
            if not files:
                logger.error("No files in request.files.getlist('files')")
                raise BadRequest("No files selected")
                
            if files[0].filename == '':
                logger.error("Empty filename in uploaded file")
                raise BadRequest("No file selected")
            
            # Create upload directory if it doesn't exist
            upload_dir = os.path.join(current_app.root_path, '..', current_app.config['UPLOAD_FOLDER'])
            try:
                os.makedirs(upload_dir, exist_ok=True)
                logger.info(f"Upload directory: {upload_dir}")
                
                # Test directory permissions
                test_file = os.path.join(upload_dir, '.permission_test')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                
            except Exception as e:
                logger.error(f"Error accessing upload directory {upload_dir}: {str(e)}")
                raise Exception(f"Cannot write to upload directory: {str(e)}")
            
            uploaded_files = []
            
            for file in files:
                try:
                    if not file or not file.filename:
                        logger.warning("Skipping empty file in upload")
                        continue
                        
                    if not allowed_file(file.filename):
                        logger.warning(f"File type not allowed: {file.filename}")
                        continue
                    
                    # Generate unique filename
                    original_filename = file.filename
                    file_extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
                    unique_filename = f"{uuid.uuid4().hex}.{file_extension}" if file_extension else f"{uuid.uuid4().hex}"
                    secure_name = secure_filename(unique_filename)
                    
                    # Save file
                    file_path = os.path.join(upload_dir, secure_name)
                    try:
                        file.save(file_path)
                        logger.info(f"Successfully saved file to {file_path}")
                    except Exception as e:
                        logger.error(f"Error saving file {original_filename}: {str(e)}")
                        continue
                    
                    # Verify file was saved
                    if not os.path.exists(file_path):
                        logger.error(f"File {file_path} was not saved successfully")
                        continue
                        
                    # Get file info
                    try:
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
                        logger.info(f"Successfully processed upload: {original_filename} as {secure_name} ({file_size} bytes)")
                        
                    except Exception as e:
                        logger.error(f"Error processing file info for {file_path}: {str(e)}")
                        if os.path.exists(file_path):
                            try:
                                os.remove(file_path)
                            except:
                                pass
                
                except Exception as e:
                    logger.error(f"Error processing file {file.filename if file else 'None'}: {str(e)}")
                    
            if not uploaded_files:
                logger.error("No files were successfully uploaded")
                raise BadRequest("No valid files were uploaded. Please check file types and try again.")
            
            # Convert the list of dictionaries to a list of serializable dictionaries
            response_data = []
            for file_info in uploaded_files:
                # Convert datetime to ISO format string if it's a datetime object
                created_at = file_info['created_at']
                if hasattr(created_at, 'isoformat'):
                    created_at = created_at.isoformat()
                
                response_data.append({
                    'filename': file_info['filename'],
                    'original_filename': file_info['original_filename'],
                    'file_size': file_info['file_size'],
                    'file_type': file_info['file_type'],
                    'upload_path': file_info['upload_path'],
                    'created_at': created_at
                })
            
            # Return raw dictionary instead of Pydantic model to avoid serialization issues
            return {
                'success': True,
                'data': response_data,
                'message': f"Successfully uploaded {len(uploaded_files)} file(s)"
            }, 200
            
        except RequestEntityTooLarge as e:
            logger.error(f"File too large: {str(e)}")
            error_response = ErrorResponse(
                message="File too large. Maximum size allowed is 100MB",
                error_code="FILE_TOO_LARGE"
            )
            return error_response.dict(), 413
            
        except BadRequest as e:
            logger.error(f"Bad request: {str(e)}")
            error_response = ErrorResponse(
                message=str(e.description) if hasattr(e, 'description') else str(e),
                error_code="BAD_REQUEST"
            )
            return error_response.dict(), 400
            
        except Exception as e:
            logger.error(f"Unexpected error in file upload: {str(e)}", exc_info=True)
            error_response = ErrorResponse(
                message=f"An error occurred while uploading files: {str(e)}",
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
