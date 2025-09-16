#!/usr/bin/env python3
"""
Test script for music database initialization and recommendation system.
This script can be used to test the music vectorization and recommendation services.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

from app.services.recommendation_service import RecommendationService
from app.services.music_vectorization_service import MusicVectorizationService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_music_vectorization():
    """Test the music vectorization service"""
    logger.info("Testing Music Vectorization Service...")
    
    try:
        # Initialize service
        music_service = MusicVectorizationService()
        
        # Test text feature extraction
        test_query = "upbeat electronic dance music"
        features = music_service.extract_text_features(test_query)
        logger.info(f"Extracted {len(features)} features for text: {test_query}")
        
        # Get collection stats
        stats = music_service.get_collection_stats()
        logger.info(f"Collection stats: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing music vectorization: {e}")
        return False

def test_recommendation_service():
    """Test the recommendation service"""
    logger.info("Testing Recommendation Service...")
    
    try:
        # Initialize service
        recommendation_service = RecommendationService()
        
        # Test text-based recommendations
        test_queries = [
            "energetic upbeat music",
            "calm relaxing ambient",
            "rock guitar heavy",
            "pop catchy melody"
        ]
        
        for query in test_queries:
            logger.info(f"Testing query: {query}")
            songs = recommendation_service.recommend_by_text_query(query, limit=5)
            logger.info(f"Found {len(songs)} recommendations")
            
            if songs:
                for i, song in enumerate(songs[:3], 1):
                    logger.info(f"  {i}. {song.title} by {', '.join(song.artists)}")
        
        # Get database stats
        stats = recommendation_service.get_database_stats()
        logger.info(f"Database stats: {stats}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing recommendation service: {e}")
        return False

def initialize_sample_database():
    """Initialize database with a small sample of videos"""
    logger.info("Initializing sample music database...")
    
    try:
        # Check if API keys are available
        youtube_api_key = os.environ.get('YOUTUBE_API_KEY')
        if not youtube_api_key:
            logger.warning("YOUTUBE_API_KEY not found. Skipping database initialization.")
            return False
        
        # Initialize service
        recommendation_service = RecommendationService()
        
        # Initialize with a small number of videos for testing
        result = recommendation_service.initialize_music_database(max_videos=10)
        logger.info(f"Database initialization result: {result}")
        
        return result.get('processed', 0) > 0
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        return False

def main():
    """Main test function"""
    logger.info("Starting music recommendation system tests...")
    
    # Check environment
    required_vars = ['QDRANT_HOST']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.info("Using default values where possible...")
    
    # Test services
    tests = [
        ("Music Vectorization Service", test_music_vectorization),
        ("Recommendation Service", test_recommendation_service),
    ]
    
    results = {}
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            results[test_name] = test_func()
        except Exception as e:
            logger.error(f"Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Optional database initialization
    logger.info(f"\n{'='*50}")
    logger.info("Optional: Database Initialization")
    logger.info(f"{'='*50}")
    
    if os.environ.get('YOUTUBE_API_KEY'):
        results["Database Initialization"] = initialize_sample_database()
    else:
        logger.info("Skipping database initialization (no YouTube API key)")
        results["Database Initialization"] = "Skipped"
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result is True else "❌ FAILED" if result is False else "⏭️ SKIPPED"
        logger.info(f"{test_name}: {status}")
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    total = len([r for r in results.values() if r is not "Skipped"])
    
    if total > 0:
        logger.info(f"\nOverall: {passed}/{total} tests passed")
        return passed == total
    else:
        logger.info("\nNo tests were run")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
