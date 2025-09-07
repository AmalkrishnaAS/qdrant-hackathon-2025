"use client";

import { useState, useRef, useEffect } from "react";
import { Play, Pause, RotateCcw, Volume2, VolumeX } from "lucide-react";

type VideoPreviewProps = {
  videoUrl: string;
};

export default function VideoPreview({ videoUrl }: VideoPreviewProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [duration, setDuration] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  const [isMuted, setIsMuted] = useState(true);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const handleLoadedMetadata = () => setDuration(video.duration || 0);
    const handleTimeUpdate = () => setCurrentTime(video.currentTime);
    const handleEnded = () => {
      setIsPlaying(false);
      setCurrentTime(0);
    };

    video.addEventListener("loadedmetadata", handleLoadedMetadata);
    video.addEventListener("timeupdate", handleTimeUpdate);
    video.addEventListener("ended", handleEnded);

    return () => {
      video.pause();
      video.removeEventListener("loadedmetadata", handleLoadedMetadata);
      video.removeEventListener("timeupdate", handleTimeUpdate);
      video.removeEventListener("ended", handleEnded);
    };
  }, [videoUrl]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
    } else {
      videoRef.current.play().catch((err) =>
        console.error("Play error:", err)
      );
    }
    setIsPlaying(!isPlaying);
  };

  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!videoRef.current || !duration) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const pos = (e.clientX - rect.left) / rect.width;
    const newTime = pos * duration;
    videoRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleReset = () => {
    if (!videoRef.current) return;
    videoRef.current.currentTime = 0;
    setCurrentTime(0);
  };

  const formatTime = (time: number) => {
    if (isNaN(time)) return "0:00";
    const m = Math.floor(time / 60);
    const s = Math.floor(time % 60);
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      <div className="relative aspect-video bg-black rounded-md overflow-hidden">
        <video
          ref={videoRef}
          src={videoUrl}
          className="w-full h-full object-contain"
          playsInline
          muted={isMuted}
        />
        {!isPlaying && (
          <button
            className="absolute inset-0 flex items-center justify-center bg-black/40 hover:bg-black/50 transition"
            onClick={togglePlay}
          >
            <Play className="w-16 h-16 text-white" />
          </button>
        )}
      </div>

      {/* Controls */}
      <div className="mt-4 flex items-center gap-2">
        <button
          className="p-2 rounded bg-secondary text-secondary-foreground hover:bg-secondary/80 transition"
          onClick={togglePlay}
        >
          {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
        </button>

        <button
          className="p-2 rounded bg-secondary text-secondary-foreground hover:bg-secondary/80 transition"
          onClick={handleReset}
        >
          <RotateCcw className="w-4 h-4" />
        </button>

        <div
          className="flex-1 h-2 bg-muted rounded cursor-pointer relative"
          onClick={handleSeek}
        >
          <div
            className="h-full bg-primary rounded"
            style={{ width: `${(currentTime / (duration || 1)) * 100}%` }}
          />
        </div>

        <span className="text-sm w-12 text-center text-muted-foreground">
          {formatTime(currentTime)}
        </span>
        <span className="text-sm w-12 text-center text-muted-foreground">
          {formatTime(duration)}
        </span>

        <button
          className="p-2 rounded bg-secondary text-secondary-foreground hover:bg-secondary/80 transition"
          onClick={() => setIsMuted(!isMuted)}
        >
          {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
        </button>
      </div>
    </div>
  );
}
