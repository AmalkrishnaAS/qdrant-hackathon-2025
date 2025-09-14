import os
import youtube_dl
import librosa
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams

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
        info = ydl.extract_info(url, download=True)
        return os.path.join(output_path, f"{info['id']}.mp3"), info

# ------------------ STEP 2: Vectorize Audio ------------------
def vectorize_audio(file_path, target_dim=1024):

# ------------------ STEP 3: Store in Qdrant ------------------
def store_in_qdrant(video_id, vector, info):
    client = QdrantClient(url=QDRANT_URL)

    # Create / reset collection
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=VectorParams(size=len(vector), distance="Cosine"),
    )

    payload = {
        "video_id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "description": info.get("description"),
        "tags": info.get("tags"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "url": info.get("webpage_url"),
    }

    point = PointStruct(
        id=video_id,
        vector=vector,
        payload=payload
    )

    client.upsert(collection_name=QDRANT_COLLECTION, points=[point])

# ------------------ MAIN ------------------
if __name__ == "__main__":
    video_id = "dQw4w9WgXcQ"  # Example

    mp3_file, info = download_audio(video_id)
    vector = vectorize_audio(mp3_file)
    store_in_qdrant(video_id, vector, info)

    print(f"✅ Stored {video_id} metadata + vector in Qdrant")
