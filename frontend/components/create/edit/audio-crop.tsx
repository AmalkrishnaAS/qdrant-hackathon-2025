"use client"

import type React from "react"
import { useState, useRef, useCallback, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Play, Pause, RotateCcw, Send, Music } from "lucide-react"
import { useCreate } from "@/context/create-context"

type AudioCropperProps = {
  audioUrl: string
  className?: string
}

declare global {
  interface Window {
    onYouTubeIframeAPIReady: () => void
    YT: any
  }
}

export function AudioCropper({ audioUrl, className = "" }: AudioCropperProps) {
  const { setActiveTab } = useCreate();
  const [player, setPlayer] = useState<any>(null)
  const [isYouTubeReady, setIsYouTubeReady] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [isPlaying, setIsPlaying] = useState(false)
  const [duration, setDuration] = useState(0)
  const [currentTime, setCurrentTime] = useState(0)
  const [windowStart, setWindowStart] = useState(0)
  const [isPreviewMode, setIsPreviewMode] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const WINDOW_DURATION = 30
  const audioPlayerRef = useRef<HTMLDivElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const timeUpdateIntervalRef = useRef<NodeJS.Timeout>(null)
  const lastTimeRef = useRef<number>(0)
  const stuckCountRef = useRef<number>(0)

  const extractVideoId = useCallback((url: string) => {
    const regex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)/
    const match = url.match(regex)
    console.log("[v0] Extracted video ID:", match ? match[1] : "none")
    return match ? match[1] : null
  }, [])

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes}:${seconds.toString().padStart(2, "0")}`
  }

  const generateSyntheticWaveform = useCallback((videoDuration: number) => {
    const canvas = canvasRef.current
    if (!canvas) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    const width = canvas.width
    const height = canvas.height
    const amp = height / 2

    ctx.fillStyle = "#ffffff"
    ctx.fillRect(0, 0, width, height)

    ctx.strokeStyle = "#a0aec0"
    ctx.lineWidth = 0.5
    ctx.beginPath()

    for (let i = 0; i < width; i++) {
      const time = (i / width) * videoDuration
      const amplitude = Math.sin(time * 0.5) * 0.5 + Math.cos(time * 2) * 0.2 + Math.random() * 0.3
      const y = amp - amplitude * amp * 0.8
      ctx.moveTo(i, amp)
      ctx.lineTo(i, y)
    }
    ctx.stroke()
  }, [])

  const drawWaveformOverlay = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas || !duration) return
    const ctx = canvas.getContext("2d")
    if (!ctx) return

    generateSyntheticWaveform(duration)

    const width = canvas.width
    const height = canvas.height
    const startX = (windowStart / duration) * width
    const endX = ((windowStart + WINDOW_DURATION) / duration) * width
    const currentX = (currentTime / duration) * width

    // Selection window
    ctx.fillStyle = "rgba(59, 130, 246, 0.2)"
    ctx.fillRect(startX, 0, endX - startX, height)
    ctx.strokeStyle = "#3b82f6"
    ctx.lineWidth = 1
    ctx.strokeRect(startX, 0, endX - startX, height)

    // Current time indicator
    ctx.strokeStyle = "#ef4444"
    ctx.lineWidth = 2
    ctx.beginPath()
    ctx.moveTo(currentX, 0)
    ctx.lineTo(currentX, height)
    ctx.stroke()
  }, [windowStart, currentTime, duration, WINDOW_DURATION, generateSyntheticWaveform])

  const loadYouTubeVideo = useCallback(() => {
    const videoId = extractVideoId(audioUrl)
    if (!videoId || !audioPlayerRef.current) {
      console.log("[v0] Cannot load YouTube video - missing video ID or ref")
      return
    }

    console.log("[v0] Loading YouTube video with ID:", videoId)
    setIsLoading(true)
    const newPlayer = new window.YT.Player(audioPlayerRef.current, {
      height: "0",
      width: "0",
      videoId: videoId,
      playerVars: { controls: 0, disablekb: 1, modestbranding: 1 },
      events: {
        onReady: (event: any) => {
          const videoDuration = event.target.getDuration()
          setDuration(videoDuration)
          setIsLoading(false)
          generateSyntheticWaveform(videoDuration)
        },
        onStateChange: (event: any) => {
          setIsPlaying(event.data === window.YT.PlayerState.PLAYING)
        },
      },
    })
    setPlayer(newPlayer)
  }, [audioUrl, extractVideoId, generateSyntheticWaveform])

  // Init API
  useEffect(() => {
    const initYouTubeAPI = () => {
      if (window.YT && window.YT.Player) {
        console.log("[v0] YouTube API already loaded")
        setIsYouTubeReady(true)
      } else {
        console.log("[v0] Loading YouTube API")
        const tag = document.createElement("script")
        tag.src = "https://www.youtube.com/iframe_api"
        document.head.appendChild(tag)
        window.onYouTubeIframeAPIReady = () => {
          console.log("[v0] YouTube API ready")
          setIsYouTubeReady(true)
        }
      }
    }
    initYouTubeAPI()

    return () => {
      if (timeUpdateIntervalRef.current) clearInterval(timeUpdateIntervalRef.current)
    }
  }, [])

  useEffect(() => {
    if (isYouTubeReady && !player) {
      loadYouTubeVideo()
    }
  }, [isYouTubeReady, player, loadYouTubeVideo])

  useEffect(() => {
    drawWaveformOverlay()

    if (player && typeof player.getCurrentTime === "function") {
      if (timeUpdateIntervalRef.current) clearInterval(timeUpdateIntervalRef.current)
      timeUpdateIntervalRef.current = setInterval(() => {
        const current = player.getCurrentTime()

        if (isPlaying && Math.abs(current - lastTimeRef.current) < 0.01) {
          stuckCountRef.current += 1
          if (stuckCountRef.current > 20) {
            console.log("[v0] Player appears stuck, attempting recovery")
            player.seekTo(current + 0.1, true)
            player.playVideo()
            stuckCountRef.current = 0
          }
        } else {
          stuckCountRef.current = 0
        }

        lastTimeRef.current = current
        setCurrentTime(current)

        if (isPreviewMode && current >= windowStart + WINDOW_DURATION) {
          player.pauseVideo()
        }
      }, 100)
    }

    return () => {
      if (timeUpdateIntervalRef.current) clearInterval(timeUpdateIntervalRef.current)
    }
  }, [player, isPreviewMode, windowStart, drawWaveformOverlay, WINDOW_DURATION, isPlaying])

  const handlePlayPause = () => {
    if (!player) return
    if (isPlaying) {
      player.pauseVideo()
    } else {
      const playStartTime = isPreviewMode && currentTime < windowStart ? windowStart : currentTime
      player.seekTo(playStartTime, true)
      setTimeout(() => {
        player.playVideo()
        stuckCountRef.current = 0
        lastTimeRef.current = playStartTime
      }, 100)
    }
  }

  const handleReset = () => {
    if (!player) return
    const seekTime = isPreviewMode ? windowStart : 0
    player.seekTo(seekTime, true)
    setCurrentTime(seekTime)
    if (isPlaying) player.pauseVideo()
  }

  const handleCanvasClick = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current
    if (!canvas || !duration) return
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const clickTime = (x / canvas.width) * duration
    const maxStart = Math.max(0, duration - WINDOW_DURATION)
    const newStart = Math.min(Math.max(0, clickTime - WINDOW_DURATION / 2), maxStart)
    setWindowStart(newStart)
    setCurrentTime(clickTime)
    if (player) player.seekTo(clickTime, true)
  }

  const submitTimestamps = async () => {
    setIsSubmitting(true)
    setSubmitSuccess(false)
    try {
      const response = await fetch("/api/audio-timestamps", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          audioUrl,
          startTime: windowStart,
          endTime: windowStart + WINDOW_DURATION,
        }),
      })
      if (response.ok) {
        setSubmitSuccess(true)
        setTimeout(() => setSubmitSuccess(false), 3000)
        setActiveTab('download')
      }
    } catch (error) {
      console.error("Error submitting timestamps:", error)
    } finally {
      setIsSubmitting(false)
    }
  }

  console.log("[v0] AudioCropper received URL:", audioUrl)

  // Don't proceed if URL is empty
  if (!audioUrl || audioUrl.trim() === "") {
    return (
      <Card className={`w-full ${className}`}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Music className="w-5 h-5 text-blue-500" />
            Audio Snippet Selector
          </CardTitle>
          <p className="text-sm text-muted-foreground">Select a 30-second window from the audio.</p>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-48 border rounded-md bg-muted">
            <div className="text-red-500 text-center">
              <p>No audio URL provided</p>
              <p className="text-sm text-gray-500 mt-1">Please provide a valid YouTube URL</p>
            </div>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className={`w-full ${className}`}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Music className="w-5 h-5 text-blue-500" />
          Audio Snippet Selector
        </CardTitle>
        <p className="text-sm text-muted-foreground">Select a 30-second window from the audio.</p>
      </CardHeader>
      <CardContent>
        <div ref={audioPlayerRef} style={{ display: "none" }} />

        {isLoading || duration === 0 ? (
          <div className="flex items-center justify-center h-48 border rounded-md bg-muted">
            <p className="text-muted-foreground animate-pulse">
              {isYouTubeReady ? "Loading Audio..." : "Initializing Player..."}
            </p>
          </div>
        ) : (
          <>
            <canvas
              ref={canvasRef}
              width={800}
              height={150}
              className="w-full border rounded-md cursor-pointer bg-white"
              onClick={handleCanvasClick}
            />
            <div className="mt-4">
              <Slider
                value={[windowStart]}
                onValueChange={([value]) => setWindowStart(value)}
                max={Math.max(0, duration - WINDOW_DURATION)}
                step={0.1}
              />
              <div className="flex justify-between text-xs text-muted-foreground mt-2">
                <span>Start: {formatTime(windowStart)}</span>
                <span>End: {formatTime(windowStart + WINDOW_DURATION)}</span>
                <span>Total: {formatTime(duration)}</span>
              </div>
            </div>
            <div className="flex items-center gap-2 mt-6">
              <Button onClick={handlePlayPause} size="icon" variant="outline" title={isPlaying ? "Pause" : "Play"}>
                {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              </Button>
              <Button onClick={handleReset} size="icon" variant="outline" title="Reset Position">
                <RotateCcw className="w-4 h-4" />
              </Button>
              <Button
                onClick={() => setIsPreviewMode(!isPreviewMode)}
                variant={isPreviewMode ? "secondary" : "outline"}
                size="sm"
              >
                Preview Window {isPreviewMode ? "On" : "Off"}
              </Button>
            </div>
            <div className="w-full mt-4">
              <Button onClick={submitTimestamps} disabled={isSubmitting} className="w-full py-6 text-base">
                <Send className="w-5 h-5 mr-2" />
                {isSubmitting ? "Processing..." : "Save Audio Selection"}
              </Button>
            </div>
            {submitSuccess && (
              <div className="mt-4 text-sm text-green-700 p-3 bg-green-50 border border-green-200 rounded-lg">
                ✅ Success! Submitted window: {formatTime(windowStart)} - {formatTime(windowStart + WINDOW_DURATION)}
              </div>
            )}
          </>
        )}
      </CardContent>
    </Card>
  )
}
