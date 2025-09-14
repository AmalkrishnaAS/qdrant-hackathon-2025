import time
from google import genai

client = genai.Client(api_key="AIzaSyBv40JxkaVJv82u649aCHoaMHfTleoRGu8")

# Upload file
myfile = client.files.upload(file="BigBuckBunny.mp4")

# Wait until file is ACTIVE
while True:
    file_status = client.files.get(name=myfile.name)
    print(f"File status: {file_status.state}")
    if file_status.state == "ACTIVE":
        break
    elif file_status.state == "FAILED":
        raise RuntimeError("File processing failed")
    time.sleep(2)  # wait 2 seconds before checking again

# Now safe to use in generate_content
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[file_status, '''
    
    You are a video analysis assistant. Watch the provided video and generate a detailed description that captures:

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
   - Match music recommendations to the video’s pacing, visuals, and vibe.  

5. **Summary for Retrieval**  
   - Create a short, metadata-style description (like a tag list) with keywords summarizing the video’s topic, vibe, and music style.  

Output format:  
- A **paragraph** describing the video.  
- A **short recommendation** for background music style.  
- A **keyword list** (comma-separated) for retrieval and categorization.  
''']
)

print(response.text)
