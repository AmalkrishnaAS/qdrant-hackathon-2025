"use client"
import { AudioCropper } from "./audio-crop"
import VideoPreview from "./video-preview"
type AudioVideoSplitterProps = {
  videoUrl: string
  audioUrl?: string
}

export function AudioVideoSplitter({
  videoUrl,
  audioUrl = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ",
}: AudioVideoSplitterProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      <VideoPreview videoUrl={videoUrl} />
      <AudioCropper audioUrl={audioUrl} />
    </div>
  )
}
