import os
import youtube_dl
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams
from googleapiclient.discovery import build

# ------------------ CONFIG ------------------
QDRANT_URL = "http://localhost:6333"  # Local Qdrant
QDRANT_COLLECTION = "youtube_audio_vectors"

# ------------------ STEP 1: Download MP3 ------------------
def download_audio(video_id, output_path="downloads"):
    os.makedirs(output_path, exist_ok=True)
    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_path}/%(id)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        return os.path.join(output_path, f"{video_id}.mp3")

# ------------------ STEP 2: Vectorize Audio ------------------
def vectorize_audio(file_path, target_dim=1024):
    return np.random.rand(target_dim).tolist()

# ------------------ STEP 3: Store in Qdrant ------------------
def store_in_qdrant(video_id, vector,metadata):
    client = QdrantClient(url=QDRANT_URL)

    # Create / reset collection using the newer recommended approach
    collection_exists = client.collection_exists(collection_name=QDRANT_COLLECTION)
    # if collection_exists:
    #     client.delete_collection(collection_name=QDRANT_COLLECTION)

    if not collection_exists:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=len(vector), distance="Cosine"),
        )

    # Create a unique ID using UUID from the video_id
    import uuid
    point_id = int(uuid.uuid4().int & (1 << 63) - 1)  # Convert to positive 63-bit integer

    point = PointStruct(
        id=point_id,
        vector=vector,
        payload={
            "video_id": video_id,
            "source": "youtube",
            **metadata
        }
    )

    client.upsert(collection_name=QDRANT_COLLECTION, points=[point])

def get_youtube_metadata(video_id: str, api_key: str) -> dict:
    youtube = build("youtube", "v3", developerKey=api_key)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()

    if not response["items"]:
        return {"error": "Video not found"}

    video = response["items"][0]

    return {
        "title": video["snippet"]["title"],
        "description": video["snippet"]["description"],
        "channelTitle": video["snippet"]["channelTitle"],
        "publishedAt": video["snippet"]["publishedAt"],
        "duration": video["contentDetails"]["duration"],  # ISO 8601 format
        "views": video["statistics"].get("viewCount"),
        "likes": video["statistics"].get("likeCount"),
        "comments": video["statistics"].get("commentCount"),
        "tags": video["snippet"].get("tags", []),
        "thumbnail": video["snippet"]["thumbnails"]["high"]["url"]
    }

# Example usage
API_KEY = "AIzaSyANQMkXP68ryQKPAwiJ3LUZoQKhzim-_-I"
video_id = "dQw4w9WgXcQ"
metadata = get_youtube_metadata(video_id, API_KEY)
print(metadata)

# ------------------ MAIN ------------------
if __name__ == "__main__":
    video_id = "uM3Bjbskv48"  # Example
    API_KEY = "AIzaSyANQMkXP68ryQKPAwiJ3LUZoQKhzim-_-I"
    metadata = get_youtube_metadata(video_id, API_KEY)
    # print(metadata)

    mp3_file = download_audio(video_id)
    vector = vectorize_audio(mp3_file)
    store_in_qdrant(video_id, vector,metadata)

    print(f"✅ Stored {video_id} metadata + vector in Qdrant")
