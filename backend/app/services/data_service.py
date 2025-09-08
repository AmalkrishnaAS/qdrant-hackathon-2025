import logging
from typing import List, Dict, Any
from app.models.schemas import Song, Thumbnail, Thumbnails
from app.services.qdrant_service import QdrantService

logger = logging.getLogger(__name__)

class DataService:
    """Service for managing song data and initialization"""
    
    def __init__(self, qdrant_service: QdrantService):
        self.qdrant_service = qdrant_service
        self.initial_songs = self._get_initial_songs_data()
    
    def _get_initial_songs_data(self) -> List[Song]:
        """Get the initial song data matching frontend data.ts"""
        songs_data = [
            {
                'id': '1',
                'title': 'Bohemian Rhapsody',
                'artists': ['Queen'],
                'album': 'A Night at the Opera',
                'duration': '5:55',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/fJ9rUzIMcZQ/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/fJ9rUzIMcZQ/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/fJ9rUzIMcZQ/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'fJ9rUzIMcZQ',
                'isExplicit': False,
                'category': 'Classic Rock',
                'description': 'A six-minute suite, notable for its lack of a refraining chorus and instead consisting of several sections',
            },
            {
                'id': '2',
                'title': 'Blinding Lights',
                'artists': ['The Weeknd'],
                'album': 'After Hours',
                'duration': '3:20',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/4NRXx6U8ABQ/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/4NRXx6U8ABQ/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/4NRXx6U8ABQ/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': '4NRXx6U8ABQ',
                'isExplicit': False,
                'category': 'Pop',
                'description': 'A synth-pop and nu-disco song with a pulsing beat and retro 1980s feel',
            },
            {
                'id': '3',
                'title': "Don't Start Now",
                'artists': ['Dua Lipa'],
                'album': 'Future Nostalgia',
                'duration': '3:03',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/oygrmJFKYZY/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/oygrmJFKYZY/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/oygrmJFKYZY/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'oygrmJFKYZY',
                'isExplicit': False,
                'category': 'Pop',
                'description': 'A disco-pop and nu-disco song with elements of 1970s disco and 1980s pop',
            },
            {
                'id': '4',
                'title': 'Watermelon Sugar',
                'artists': ['Harry Styles'],
                'album': 'Fine Line',
                'duration': '2:54',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/E07s5ZYygMg/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/E07s5ZYygMg/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/E07s5ZYygMg/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'E07s5ZYygMg',
                'isExplicit': False,
                'category': 'Pop Rock',
                'description': 'A pop rock and soft rock song with elements of funk and psychedelic pop',
            },
            {
                'id': '5',
                'title': 'Levitating',
                'artists': ['Dua Lipa', 'DaBaby'],
                'album': 'Future Nostalgia',
                'duration': '3:23',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/TUVcZxfQlFY/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/TUVcZxfQlFY/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/TUVcZxfQlFY/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'TUVcZxfQlFY',
                'isExplicit': False,
                'category': 'Pop',
                'description': 'A disco-pop and dance-pop song with elements of 1970s and 1980s dance music',
            },
            {
                'id': '6',
                'title': 'Save Your Tears',
                'artists': ['The Weeknd'],
                'album': 'After Hours',
                'duration': '3:35',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/XXYlFuWEuKI/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/XXYlFuWEuKI/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/XXYlFuWEuKI/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'XXYlFuWEuKI',
                'isExplicit': False,
                'category': 'Pop',
                'description': 'A synth-pop and new wave song with a retro 1980s feel',
            },
            {
                'id': '7',
                'title': 'Stay',
                'artists': ['The Kid LAROI', 'Justin Bieber'],
                'album': 'F*CK LOVE 3: OVER YOU',
                'duration': '2:21',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/kTJczUoc26U/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/kTJczUoc26U/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/kTJczUoc26U/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'kTJczUoc26U',
                'isExplicit': True,
                'category': 'Pop',
                'description': 'A pop and emo rap song with a melancholic yet catchy melody',
            },
            {
                'id': '8',
                'title': 'good 4 u',
                'artists': ['Olivia Rodrigo'],
                'album': 'SOUR',
                'duration': '2:58',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/gNi_6U5Pm_o/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/gNi_6U5Pm_o/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/gNi_6U5Pm_o/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'gNi_6U5Pm_o',
                'isExplicit': True,
                'category': 'Pop Punk',
                'description': 'A pop-punk and pop-rock song with angsty lyrics and a driving beat',
            },
            {
                'id': '9',
                'title': 'Montero',
                'artists': ['Lil Nas X'],
                'album': 'MONTERO',
                'duration': '2:17',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/6swmTBVIpgk/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/6swmTBVIpgk/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/6swmTBVIpgk/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': '6swmTBVIpgk',
                'isExplicit': True,
                'category': 'Pop Rap',
                'description': 'A pop-rap and trap song with a catchy melody and controversial themes',
            },
            {
                'id': '10',
                'title': 'Peaches',
                'artists': ['Justin Bieber', 'Daniel Caesar', 'Giveon'],
                'album': 'Justice',
                'duration': '3:18',
                'thumbnails': {
                    'default': {'url': 'https://img.youtube.com/vi/tQ0yjYUFKae/default.jpg', 'width': 120, 'height': 90},
                    'medium': {'url': 'https://img.youtube.com/vi/tQ0yjYUFKae/mqdefault.jpg', 'width': 320, 'height': 180},
                    'high': {'url': 'https://img.youtube.com/vi/tQ0yjYUFKae/hqdefault.jpg', 'width': 480, 'height': 360},
                },
                'videoId': 'tQ0yjYUFKae',
                'isExplicit': False,
                'category': 'R&B',
                'description': 'A smooth R&B track with melodic vocals and a laid-back vibe',
            },
        ]
        
        songs = []
        for song_data in songs_data:
            # Convert thumbnail data to Pydantic models
            thumbnails = Thumbnails(
                default=Thumbnail(**song_data['thumbnails']['default']),
                medium=Thumbnail(**song_data['thumbnails']['medium']),
                high=Thumbnail(**song_data['thumbnails']['high'])
            )
            
            song = Song(
                id=song_data['id'],
                title=song_data['title'],
                artists=song_data['artists'],
                album=song_data['album'],
                duration=song_data['duration'],
                thumbnails=thumbnails,
                videoId=song_data['videoId'],
                isExplicit=song_data['isExplicit'],
                category=song_data['category'],
                description=song_data['description']
            )
            songs.append(song)
        
        return songs
    
    def initialize_data(self) -> bool:
        """Initialize Qdrant with seed data"""
        try:
            logger.info("Initializing Qdrant with seed data...")
            
            # Check if data already exists
            collection_info = self.qdrant_service.get_collection_info()
            if collection_info.get("points_count", 0) > 0:
                logger.info(f"Collection already has {collection_info['points_count']} points. Skipping initialization.")
                return True
            
            # Add initial songs to Qdrant
            added_count = self.qdrant_service.add_songs_batch(self.initial_songs)
            
            if added_count > 0:
                logger.info(f"Successfully initialized {added_count} songs in Qdrant")
                return True
            else:
                logger.error("Failed to initialize songs in Qdrant")
                return False
                
        except Exception as e:
            logger.error(f"Error initializing data: {e}")
            return False
    
    def get_all_songs(self) -> List[Song]:
        """Get all initial songs"""
        return self.initial_songs
    
    def get_song_by_id(self, song_id: str) -> Song | None:
        """Get a specific song by ID"""
        for song in self.initial_songs:
            if song.id == song_id:
                return song
        return None

