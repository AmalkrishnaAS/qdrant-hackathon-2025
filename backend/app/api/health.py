from flask_restx import Namespace, Resource, fields
from flask import current_app
from app.models.schemas import HealthResponse
from app.services.qdrant_service import QdrantService
import logging

logger = logging.getLogger(__name__)

# Create namespace
api = Namespace('health', description='Health check operations')

# Define response models for Swagger
health_model = api.model('Health', {
    'status': fields.String(required=True, description='Service status'),
    'version': fields.String(required=True, description='API version'),
    'timestamp': fields.DateTime(required=True, description='Current timestamp'),
    'services': fields.Raw(description='Status of dependent services')
})

@api.route('/')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(health_model)
    def get(self):
        """
        Health check endpoint
        Returns the current status of the API and its dependencies
        """
        try:
            # Initialize Qdrant service for health check
            qdrant_service = QdrantService(
                host=current_app.config['QDRANT_HOST'],
                port=current_app.config['QDRANT_PORT'],
                api_key=current_app.config.get('QDRANT_API_KEY')
            )
            
            # Check Qdrant health
            qdrant_healthy = qdrant_service.health_check()
            
            response = HealthResponse(
                status="healthy" if qdrant_healthy else "degraded",
                version=current_app.config['API_VERSION'],
                services={
                    "qdrant": qdrant_healthy,
                    "api": True
                }
            )
            
            return response.dict(), 200 if qdrant_healthy else 503
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            response = HealthResponse(
                status="unhealthy",
                version=current_app.config.get('API_VERSION', '1.0.0'),
                services={
                    "qdrant": False,
                    "api": True
                }
            )
            return response.dict(), 503

