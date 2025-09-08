#!/usr/bin/env python3
"""
Startup script for the Flask backend application
"""
import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def check_qdrant_connection():
    """Check if Qdrant is running and accessible"""
    try:
        from app.services.qdrant_service import QdrantService
        
        qdrant_service = QdrantService(
            host=os.getenv('QDRANT_HOST', 'localhost'),
            port=int(os.getenv('QDRANT_PORT', 6333)),
            api_key=os.getenv('QDRANT_API_KEY')
        )
        
        if qdrant_service.health_check():
            logger.info("✓ Qdrant connection successful")
            return True
        else:
            logger.error("✗ Qdrant connection failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Qdrant connection error: {e}")
        return False

def initialize_data():
    """Initialize Qdrant with seed data"""
    try:
        from app.services.qdrant_service import QdrantService
        from app.services.data_service import DataService
        
        qdrant_service = QdrantService(
            host=os.getenv('QDRANT_HOST', 'localhost'),
            port=int(os.getenv('QDRANT_PORT', 6333)),
            api_key=os.getenv('QDRANT_API_KEY')
        )
        
        data_service = DataService(qdrant_service)
        
        if data_service.initialize_data():
            logger.info("✓ Data initialization successful")
            return True
        else:
            logger.error("✗ Data initialization failed")
            return False
            
    except Exception as e:
        logger.error(f"✗ Data initialization error: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("🚀 Starting Qdrant Hackathon Backend...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        logger.error("✗ Python 3.8+ required")
        sys.exit(1)
    
    logger.info(f"✓ Python {sys.version.split()[0]}")
    
    # Check Qdrant connection
    if not check_qdrant_connection():
        logger.error("❌ Please start Qdrant first:")
        logger.error("   docker run -p 6333:6333 qdrant/qdrant")
        sys.exit(1)
    
    # Initialize data
    if not initialize_data():
        logger.warning("⚠️  Data initialization failed, but continuing...")
    
    # Import and create app
    try:
        from app import create_app
        app = create_app()
        
        # Print available routes
        logger.info("📍 Available API endpoints:")
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':
                logger.info(f"   {rule.methods} {rule.rule}")
        
        logger.info("📖 API Documentation: http://localhost:5001/docs/")
        logger.info("🔍 Health Check: http://localhost:5001/api/health/")
        logger.info("🎵 Trending Songs: http://localhost:5001/api/songs/trending")
        
        # Start the Flask development server on port 5001 to avoid macOS AirPlay conflict
        app.run(
            host='0.0.0.0',
            port=int(os.getenv('PORT', 5001)),
            debug=os.getenv('DEBUG', 'True').lower() == 'true'
        )
        
    except ImportError as e:
        logger.error(f"✗ Import error: {e}")
        logger.error("   Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

