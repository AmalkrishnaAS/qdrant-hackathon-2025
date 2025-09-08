import { apiClient } from '@/lib/api-client';
import { logError, logInfo } from '@/lib/logger';

export interface MappedItem {
  id: string;
  title: string;
  artists: string[];
  album: string;
  duration: string;
  thumbnails: {
    default: { url: string; width: number; height: number };
    medium: { url: string; width: number; height: number };
    high: { url: string; width: number; height: number };
  };
  videoId: string;
  isExplicit: boolean;
  category: string;
  description: string;
}

function parseIsoDurationToMmSs(iso: string | undefined): string {
  if (!iso) return '0:00';
  const match = /PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/.exec(iso);
  if (!match) return '0:00';
  const hours = parseInt(match[1] ?? '0', 10);
  const minutes = parseInt(match[2] ?? '0', 10) + hours * 60;
  const seconds = parseInt(match[3] ?? '0', 10);
  const mm = String(minutes);
  const ss = String(seconds).padStart(2, '0');
  return `${mm}:${ss}`;
}

export async function fetchYouTubeItems(options: {
  apiKey?: string;
  query?: string;
  maxPool?: number; // how many to sample from before picking count
  count?: number; // how many results to returnS
  regionCode?: string; // for trending
}): Promise<MappedItem[]> {
  const envKey = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY;
  const { apiKey: apiKeyFromOptions, query, maxPool = 25, count = 10, regionCode = 'US' } = options;
  const apiKey = apiKeyFromOptions ?? envKey;

  if (!apiKey) {
    logError('YouTube API key missing');
    return [];
  }
  
  // When query is provided, use Search API then fetch details
  if (query && query.trim().length > 0) {
    let searchRes: any;
    try {
      searchRes = await apiClient.get('https://www.googleapis.com/youtube/v3/search', {
        headers: { Authorization: '' },
        params: {
          key: apiKey,
          part: 'snippet',
          maxResults: maxPool,
          q: query.trim(),
          type: 'video',
          videoCategoryId: 10,
        },
      });
    } catch (error) {
      logError('YouTube search request failed', error, { query });
      throw error;
    }

    const candidates: any[] = Array.isArray((searchRes as any)?.data?.items)
      ? (searchRes as any).data.items
      : [];
    if (candidates.length === 0) return [];

    const picked = candidates.slice(0, count);
    const videoIds = picked.map((v: any) => v?.id?.videoId).filter(Boolean);
    if (videoIds.length === 0) return [];

    let detailsRes: any;
    try {
      detailsRes = await apiClient.get('https://www.googleapis.com/youtube/v3/videos', {
        headers: { Authorization: '' },
        params: {
          key: apiKey,
          part: 'snippet,contentDetails',
          id: videoIds.join(','),
        },
      });
    } catch (error) {
      logError('YouTube details request failed', error, { videoIdsCount: videoIds.length });
      throw error;
    }

    const detailsById: Record<string, any> = {};
    for (const v of ((detailsRes as any)?.data?.items ?? [])) {
      detailsById[v.id] = v;
    }

    return picked.map((s: any, idx: number) => {
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
      } as MappedItem;
    });
  }

  // Otherwise fetch trending most popular music videos
  let trendingRes: any;
  try {
    trendingRes = await apiClient.get('https://www.googleapis.com/youtube/v3/videos', {
      headers: { Authorization: '' },
      params: {
        key: apiKey,
        part: 'snippet,contentDetails',
        chart: 'mostPopular',
        regionCode,
        videoCategoryId: 10,
        maxResults: maxPool,
      },
    });
  } catch (error) {
    logError('YouTube trending request failed', error, { regionCode });
    throw error;
  }

  const candidates: any[] = Array.isArray((trendingRes as any)?.data?.items)
    ? (trendingRes as any).data.items
    : [];
  if (candidates.length === 0) return [];

  const picked = candidates.slice(0, count);

  return picked.map((s: any, idx: number) => {
    const vid = s.id ?? String(idx);
    const snippet = s?.snippet ?? {};
    const contentDetails = s?.contentDetails ?? {};
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
    } as MappedItem;
  });
}


