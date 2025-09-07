"use client"
import { AudioCropper } from "./audio-crop"
import VideoPreview from "./video-preview"
import { useCreate } from "@/context/create-context"

type AudioVideoSplitterProps = {
  videoUrl: string
  audioUrl?: string
}

export function AudioVideoSplitter({
  videoUrl,
  audioUrl,
}: AudioVideoSplitterProps) {
  const { selectedTrack } = useCreate()
  
  // Use the selected track's videoId if available, otherwise fall back to the prop or default
  const audioSrc = selectedTrack?.videoId 
    ? `https://www.youtube.com/watch?v=${selectedTrack.videoId}`
    : audioUrl || "https://www.youtube.com/watch?v=mHoohmMCR4w"
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      <VideoPreview videoUrl={videoUrl} />
      <AudioCropper audioUrl={audioSrc} />
    </div>
  )
}
