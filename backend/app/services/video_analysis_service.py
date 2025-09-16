import os
import time
import logging
from typing import Dict, List, Optional, Any
import google.generativeai as genai
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)

class VideoAnalysisService:
    """Service for analyzing videos using Gemini AI to generate music recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the video analysis service with Gemini API key"""
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is required for video analysis")
        
        genai.configure(api_key=self.api_key)
        
    def analyze_video(self, video_path: str, timeout: int = 300) -> Dict[str, Any]:
        """
        Analyze a video file and generate detailed description for music matching
        
        Args:
            video_path: Path to the video file
            timeout: Maximum time to wait for processing (seconds)
            
        Returns:
            Dict containing video analysis results
        """
        try:
            logger.info(f"Starting video analysis for: {video_path}")
            
            # Upload file to Gemini
            myfile = genai.upload_file(video_path)
            logger.info(f"File uploaded with name: {myfile.name}")
            
            # Wait for file to be processed
            start_time = time.time()
            while time.time() - start_time < timeout:
                file_status = genai.get_file(myfile.name)
                logger.info(f"File status: {file_status.state}")
                
                if file_status.state.name == "ACTIVE":
                    break
                elif file_status.state.name == "FAILED":
                    raise RuntimeError("File processing failed")
                
                time.sleep(2)  # Wait 2 seconds before checking again
            else:
                raise TimeoutError(f"File processing timeout after {timeout} seconds")
            
            # Generate analysis
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([
                file_status, 
                self._get_analysis_prompt()
            ])
            
            # Parse the response
            analysis_text = response.text
            logger.info("Video analysis completed successfully")
            
            # Parse the structured response
            parsed_analysis = self._parse_analysis_response(analysis_text)
            
            # Clean up uploaded file
            try:
                genai.delete_file(myfile.name)
                logger.info("Uploaded file cleaned up")
            except Exception as e:
                logger.warning(f"Failed to clean up uploaded file: {e}")
            
            return parsed_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing video: {e}")
            raise
    
    def _get_analysis_prompt(self) -> str:
        """Get the prompt for video analysis"""
        return '''
You are a video analysis assistant specialized in matching videos to background music. Watch the provided video and generate a detailed description that captures:

1. **Content & Narrative**  
   - What is happening in the video?  
   - Who/what appears (people, objects, locations)?  
   - Key actions or events.  

2. **Visual Style & Atmosphere**  
   - Lighting (bright, dark, moody, natural).  
   - Color palette and dominant tones.  
   - Cinematography style (fast cuts, slow pans, handheld, cinematic, vlog-like).  
   - Overall pacing (fast, calm, energetic, suspenseful).  

3. **Emotional Vibe & Feel**  
   - The mood conveyed (happy, nostalgic, intense, relaxing, dramatic, inspirational).  
   - Any emotions the audience is likely to feel.  

4. **Audio & Music Cues**  
   - If music is present: genre, tempo, instruments, and emotional tone.  
   - If no music: suggest the type of background music that would best fit the video (e.g., upbeat pop, lo-fi hip-hop, cinematic orchestral, suspenseful electronic).  
   - Match music recommendations to the video's pacing, visuals, and vibe.  

5. **Summary for Retrieval**  
   - Create a short, metadata-style description (like a tag list) with keywords summarizing the video's topic, vibe, and music style.  

Please format your response as follows:
DESCRIPTION: [A paragraph describing the video]
MUSIC_RECOMMENDATION: [Short recommendation for background music style]
KEYWORDS: [Comma-separated keywords for retrieval]
MOOD: [Primary mood/emotion]
GENRE_SUGGESTIONS: [Comma-separated music genres that would fit]
TEMPO: [Slow/Medium/Fast]
ENERGY_LEVEL: [Low/Medium/High]
'''
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the structured response from Gemini"""
        try:
            lines = response_text.strip().split('\n')
            parsed = {
                'description': '',
                'music_recommendation': '',
                'keywords': [],
                'mood': '',
                'genre_suggestions': [],
                'tempo': 'Medium',
                'energy_level': 'Medium',
                'raw_response': response_text
            }
            
            current_section = None
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if line.startswith('DESCRIPTION:'):
                    parsed['description'] = line.replace('DESCRIPTION:', '').strip()
                elif line.startswith('MUSIC_RECOMMENDATION:'):
                    parsed['music_recommendation'] = line.replace('MUSIC_RECOMMENDATION:', '').strip()
                elif line.startswith('KEYWORDS:'):
                    keywords_str = line.replace('KEYWORDS:', '').strip()
                    parsed['keywords'] = [k.strip() for k in keywords_str.split(',') if k.strip()]
                elif line.startswith('MOOD:'):
                    parsed['mood'] = line.replace('MOOD:', '').strip()
                elif line.startswith('GENRE_SUGGESTIONS:'):
                    genres_str = line.replace('GENRE_SUGGESTIONS:', '').strip()
                    parsed['genre_suggestions'] = [g.strip() for g in genres_str.split(',') if g.strip()]
                elif line.startswith('TEMPO:'):
                    parsed['tempo'] = line.replace('TEMPO:', '').strip()
                elif line.startswith('ENERGY_LEVEL:'):
                    parsed['energy_level'] = line.replace('ENERGY_LEVEL:', '').strip()
            
            # If parsing failed, use the full response as description
            if not parsed['description'] and not parsed['music_recommendation']:
                parsed['description'] = response_text
                parsed['music_recommendation'] = "General background music"
                parsed['keywords'] = ['video', 'content', 'background music']
                parsed['mood'] = 'neutral'
                parsed['genre_suggestions'] = ['pop', 'electronic', 'ambient']
            
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing analysis response: {e}")
            # Return a fallback response
            return {
                'description': response_text,
                'music_recommendation': 'General background music',
                'keywords': ['video', 'content'],
                'mood': 'neutral',
                'genre_suggestions': ['pop', 'electronic'],
                'tempo': 'Medium',
                'energy_level': 'Medium',
                'raw_response': response_text
            }
    
    def generate_search_query(self, analysis: Dict[str, Any]) -> str:
        """Generate a search query for music recommendation based on video analysis"""
        try:
            # Combine different aspects of the analysis into a search query
            query_parts = []
            
            # Add mood and energy
            if analysis.get('mood'):
                query_parts.append(analysis['mood'])
            
            if analysis.get('energy_level'):
                query_parts.append(f"{analysis['energy_level']} energy")
            
            # Add genre suggestions
            if analysis.get('genre_suggestions'):
                query_parts.extend(analysis['genre_suggestions'][:2])  # Take top 2 genres
            
            # Add keywords
            if analysis.get('keywords'):
                query_parts.extend(analysis['keywords'][:3])  # Take top 3 keywords
            
            # Add tempo
            if analysis.get('tempo'):
                query_parts.append(f"{analysis['tempo']} tempo")
            
            # Combine into a search query
            search_query = ' '.join(query_parts)
            
            # Fallback if query is empty
            if not search_query.strip():
                search_query = analysis.get('music_recommendation', 'background music')
            
            logger.info(f"Generated search query: {search_query}")
            return search_query
            
        except Exception as e:
            logger.error(f"Error generating search query: {e}")
            return "background music"
