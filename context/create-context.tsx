'use client'

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { apiClient } from '@/lib/api-client';

interface CreateContextType {
  // Tab state
  activeTab: string;
  setActiveTab: (tab: string) => void;
  
  // Files state
  files: File[];
  addFiles: (newFiles: File[]) => void;
  removeFile: (index: number) => void;
  clearFiles: () => void;
  
  // Track items state
  items: any[];
  setItems: (items: any[]) => void;
  selectedTrack: any | null;
  setSelectedTrack: (track: any | null) => void;
  
  // Recommendations
  isLoading: boolean;
  handleGetRecommendations: (defaultItems: any[]) => Promise<void>;
}

const CreateContext = createContext<CreateContextType | undefined>(undefined);

export const CreateProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState<string>('upload');
  const [files, setFiles] = useState<File[]>([]);
  const [items, setItems] = useState<any[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const addFiles = (newFiles: File[]) => {
    setFiles(prevFiles => [...prevFiles, ...newFiles]);
  };

  const removeFile = (index: number) => {
    setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
  };

  const clearFiles = () => {
    setFiles([]);
  };

  const handleGetRecommendations = async (_defaultItems: any[]) => {
    try {
      setIsLoading(true);

      const apiKey = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY;
      if (!apiKey) {
        throw new Error('Missing NEXT_PUBLIC_YOUTUBE_API_KEY');
      }

      // Hardcoded search query
      const query = 'ed sheeran';

      // 1) Search for videos by hardcoded query
      const searchRes = await apiClient.get('https://www.googleapis.com/youtube/v3/search', {
        headers: { Authorization: '' },
        params: {
          key: apiKey,
          part: 'snippet',
          maxResults: 25,
          q: query,
          type: 'video',
          videoCategoryId: 10,
        },
      });

      const candidates: any[] = Array.isArray((searchRes as any)?.data?.items)
        ? (searchRes as any).data.items
        : [];
      if (candidates.length === 0) {
        setItems([]);
        return;
      }

      // 2) Pick 10 results and gather video IDs
      // const picked = candidates.slice(0, 10);
      const videoIds = candidates.map((v: any) => v?.id?.videoId).filter(Boolean);
      if (videoIds.length === 0) {
        setItems([]);
        return;
      }

      // 3) Fetch details for duration/contentDetails
      const detailsRes = await apiClient.get('https://www.googleapis.com/youtube/v3/videos', {
        headers: { Authorization: '' },
        params: {
          key: apiKey,
          part: 'snippet,contentDetails',
          id: videoIds.join(','),
        },
      });

      const detailsById: Record<string, any> = {};
      for (const v of ((detailsRes as any)?.data?.items ?? [])) {
        detailsById[v.id] = v;
      }

      // 4) Map to local Item shape
      const parseIsoDurationToMmSs = (iso: string | undefined): string => {
        if (!iso) return '0:00';
        // Basic ISO8601 PT#M#S parser
        const match = /PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/.exec(iso);
        if (!match) return '0:00';
        const hours = parseInt(match[1] ?? '0', 10);
        const minutes = parseInt(match[2] ?? '0', 10) + hours * 60;
        const seconds = parseInt(match[3] ?? '0', 10);
        const mm = String(minutes);
        const ss = String(seconds).padStart(2, '0');
        return `${mm}:${ss}`;
      };

      const mapped = candidates.map((s: any, idx: number) => {
        const vid = s.id?.videoId ?? String(idx);
        const d = detailsById[vid];
        const snippet = d?.snippet ?? s?.snippet ?? {};
        const contentDetails = d?.contentDetails ?? {};
        const thumbs = snippet?.thumbnails ?? {};
        const title: string = snippet?.title ?? 'Unknown Title';
        const channel: string = snippet?.channelTitle ?? 'Unknown Artist';
        const description: string = snippet?.description ?? '';
        const duration: string = parseIsoDurationToMmSs(contentDetails?.duration);

        return {
          id: vid,
          title,
          artists: [channel],
          album: '',
          duration,
          thumbnails: {
            default: {
              url: thumbs?.default?.url ?? '',
              width: thumbs?.default?.width ?? 120,
              height: thumbs?.default?.height ?? 90,
            },
            medium: {
              url: thumbs?.medium?.url ?? '',
              width: thumbs?.medium?.width ?? 320,
              height: thumbs?.medium?.height ?? 180,
            },
            high: {
              url: thumbs?.high?.url ?? '',
              width: thumbs?.high?.width ?? 480,
              height: thumbs?.high?.height ?? 360,
            },
          },
          videoId: vid,
          isExplicit: false,
          category: 'Music',
          description,
        };
      });

      console.log(mapped)

      setItems(mapped);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
      throw error;
    } finally {
      setIsLoading(false);
      console.log(items)
    }
  };

  const value = {
    activeTab,
    setActiveTab,
    files,
    addFiles,
    removeFile,
    clearFiles,
    items,
    setItems,
    selectedTrack,
    setSelectedTrack,
    isLoading,
    handleGetRecommendations
  };

  return (
    <CreateContext.Provider value={value}>
      {children}
    </CreateContext.Provider>
  );
};

export const useCreate = () => {
  const context = useContext(CreateContext);
  if (context === undefined) {
    throw new Error('useCreate must be used within a CreateProvider');
  }
  return context;
};
