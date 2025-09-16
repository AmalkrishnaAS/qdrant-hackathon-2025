#!/usr/bin/env python3
"""
Example usage of the AI-powered music recommendation system.
This script demonstrates how to use the various services programmatically.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_text_recommendations():
    """Example: Get music recommendations from text descriptions"""
    print("\n" + "="*60)
    print("TEXT-BASED MUSIC RECOMMENDATIONS")
    print("="*60)
    
    try:
        from app.services.recommendation_service import RecommendationService
        
        # Initialize service
        rec_service = RecommendationService()
        
        # Example queries
        queries = [
            "energetic workout music with heavy bass",
            "calm ambient music for meditation",
            "upbeat pop music for party videos",
            "dramatic orchestral music for movie scenes",
            "lo-fi hip hop for studying"
        ]
        
        for query in queries:
            print(f"\nQuery: '{query}'")
            print("-" * 50)
            
            try:
                songs = rec_service.recommend_by_text_query(query, limit=3)
                
                if songs:
                    for i, song in enumerate(songs, 1):
                        print(f"{i}. {song.title}")
                        print(f"   Artist: {', '.join(song.artists)}")
                        print(f"   Duration: {song.duration}")
                        print(f"   Video ID: {song.videoId}")
                        print()
                else:
                    print("   No recommendations found (database may be empty)")
                    
            except Exception as e:
                print(f"   Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error in text recommendations example: {e}")
        return False

def example_database_stats():
    """Example: Get database statistics"""
    print("\n" + "="*60)
    print("DATABASE STATISTICS")
    print("="*60)
    
    try:
        from app.services.recommendation_service import RecommendationService
        
        rec_service = RecommendationService()
        stats = rec_service.get_database_stats()
        
        print(f"Collection Name: {stats.get('collection_name', 'N/A')}")
        print(f"Total Vectors: {stats.get('vectors_count', 0)}")
        print(f"Total Points: {stats.get('points_count', 0)}")
        print(f"Status: {stats.get('status', 'unknown')}")
        
        if stats.get('vectors_count', 0) == 0:
            print("\nNote: Database appears to be empty.")
            print("Run the initialization to populate with trending music:")
            print("  python example_usage.py --init-db")
        
        return True
        
    except Exception as e:
        print(f"Error getting database stats: {e}")
        return False

def example_initialize_database():
    """Example: Initialize database with trending music"""
    print("\n" + "="*60)
    print("DATABASE INITIALIZATION")
    print("="*60)
    
    try:
        from app.services.recommendation_service import RecommendationService
        
        # Check for required API keys
        youtube_key = os.environ.get('YOUTUBE_API_KEY')
        if not youtube_key:
            print("Error: YOUTUBE_API_KEY environment variable is required")
            print("Please set your YouTube Data API v3 key in the .env file")
            return False
        
        rec_service = RecommendationService()
        
        print("Initializing database with trending music videos...")
        print("This may take several minutes depending on the number of videos.")
        print("Processing 10 videos for demo purposes...\n")
        
        # Initialize with a small number for demo
        result = rec_service.initialize_music_database(max_videos=10)
        
        print(f"\nInitialization complete!")
        print(f"Successfully processed: {result.get('processed', 0)} videos")
        print(f"Failed: {result.get('failed', 0)} videos")
        
        return result.get('processed', 0) > 0
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

def example_music_search():
    """Example: Direct music search using vectorization service"""
    print("\n" + "="*60)
    print("DIRECT MUSIC SEARCH")
    print("="*60)
    
    try:
        from app.services.music_vectorization_service import MusicVectorizationService
        
        music_service = MusicVectorizationService()
        
        # Test queries
        queries = [
            "electronic dance music",
            "acoustic guitar ballad",
            "jazz piano instrumental"
        ]
        
        for query in queries:
            print(f"\nSearching for: '{query}'")
            print("-" * 40)
            
            try:
                results = music_service.search_similar_music(query, limit=3)
                
                if results:
                    for i, result in enumerate(results, 1):
                        print(f"{i}. {result.get('title', 'Unknown Title')}")
                        print(f"   Channel: {result.get('channelTitle', 'Unknown')}")
                        print(f"   Score: {result.get('score', 0):.3f}")
                        print(f"   Video ID: {result.get('video_id', 'N/A')}")
                        print()
                else:
                    print("   No results found (database may be empty)")
                    
            except Exception as e:
                print(f"   Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"Error in music search example: {e}")
        return False

def main():
    """Main example runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Music Recommendation System Examples")
    parser.add_argument('--init-db', action='store_true', help='Initialize database with trending music')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--text-rec', action='store_true', help='Run text-based recommendations')
    parser.add_argument('--music-search', action='store_true', help='Run direct music search')
    parser.add_argument('--all', action='store_true', help='Run all examples')
    
    args = parser.parse_args()
    
    print("AI-Powered Music Recommendation System - Examples")
    print("=" * 60)
    
    # Check environment
    required_vars = ['QDRANT_HOST']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {missing_vars}")
        print("Using default values where possible...\n")
    
    examples_to_run = []
    
    if args.init_db or args.all:
        examples_to_run.append(('Database Initialization', example_initialize_database))
    
    if args.stats or args.all:
        examples_to_run.append(('Database Statistics', example_database_stats))
    
    if args.text_rec or args.all:
        examples_to_run.append(('Text Recommendations', example_text_recommendations))
    
    if args.music_search or args.all:
        examples_to_run.append(('Music Search', example_music_search))
    
    if not examples_to_run:
        # Default: show stats and text recommendations
        examples_to_run = [
            ('Database Statistics', example_database_stats),
            ('Text Recommendations', example_text_recommendations)
        ]
    
    # Run examples
    results = {}
    for name, func in examples_to_run:
        try:
            results[name] = func()
        except KeyboardInterrupt:
            print(f"\n\nInterrupted during: {name}")
            break
        except Exception as e:
            print(f"Error in {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for name, result in results.items():
        status = "✅ SUCCESS" if result else "❌ FAILED"
        print(f"{name}: {status}")
    
    print("\nFor more examples and API usage, see:")
    print("- Backend API documentation: http://localhost:5000/docs/")
    print("- README_AI.md for detailed AI service documentation")
    print("- test_music_db.py for comprehensive service testing")

if __name__ == "__main__":
    main()
