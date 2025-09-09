"use client";

import React, { useEffect, useMemo, useState } from 'react';
import ExpandableCardDemo from '@/components/expandable-card-demo-grid';
import Title from '@/components/title';
import { fetchYouTubeItems, MappedItem } from '@/lib/youtube';

// Initial State Component (when search box is empty)
const InitialState = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="mb-8">
        <svg
          className="w-32 h-32 text-muted-foreground/30"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>
      <h2 className="text-2xl font-semibold text-foreground mb-3">
        Discover Your Next Favorite Song
      </h2>
      <p className="text-muted-foreground max-w-lg mb-8 text-lg">
        Search through millions of songs, artists, and albums. Start typing to explore the world of music.
      </p>
    </div>
  );
};

// Empty Results State Component
const EmptyResultsState = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="mb-6">
        <svg
          className="w-24 h-24 text-muted-foreground/50"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.291-1.007-5.691-2.566M15 12a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
      </div>
      <h3 className="text-xl font-semibold text-foreground mb-2">
        No results found
      </h3>
      <p className="text-muted-foreground max-w-md">
        We couldn't find any songs, artists, or albums matching your search. Try different keywords or check your spelling.
      </p>
      <div className="mt-6 text-sm text-muted-foreground">
        <p>Try searching for:</p>
        <div className="flex flex-wrap gap-2 mt-2 justify-center">
          <span className="px-3 py-1 bg-muted rounded-full text-xs">Popular artists</span>
          <span className="px-3 py-1 bg-muted rounded-full text-xs">Song titles</span>
          <span className="px-3 py-1 bg-muted rounded-full text-xs">Album names</span>
        </div>
      </div>
    </div>
  );
};

const ExplorePage = () => {
  const [query, setQuery] = useState<string>('');
  const [results, setResults] = useState<MappedItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const apiKey = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY;

  // Debounced query value
  const debouncedQuery = useDebounce(query, 400);

  useEffect(() => {
    let isActive = true;

    async function run() {
      if (!debouncedQuery || debouncedQuery.trim().length < 2) {
        if (isActive) {
          setResults([]);
          setError(null);
          setLoading(false);
        }
        return;
      }

      if (!apiKey) {
        setError('Missing YouTube API key.');
        setLoading(false);
        return;
      }

      setLoading(true);
      setError(null);
      try {
        const items = await fetchYouTubeItems({ apiKey, query: debouncedQuery, maxPool: 25, count: 12 });
        if (isActive) setResults(items as any);
      } catch (e: any) {
        if (isActive) setError(e?.message ?? 'Search failed');
      } finally {
        if (isActive) setLoading(false);
      }
    }

    run();
    return () => {
      isActive = false;
    };
  }, [debouncedQuery, apiKey]);

  const subtitle = useMemo(() => {
    if (loading) return 'Searching...';
    if (error) return error;
    if (!query || query.trim().length < 2) return 'Type at least 2 characters to search YouTube Music';
    return `Results for "${query.trim()}" (${results.length})`;
  }, [loading, error, query, results.length]);

  return (
    <div className='p-4 md:p-12 mt-20 max-w-7xl mx-auto pb-8'>
      <Title title="Explore" description={subtitle} />

      <div className='mt-4 mb-6'>
        <label htmlFor='search' className='sr-only'>Search</label>
        <input
          id='search'
          type='text'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='Search songs, artists, albums...'
          className='w-full rounded-xl border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-orange-500'
        />
      </div>

      {!query || query.trim().length < 2 ? (
        <InitialState />
      ) : !loading && !error && results.length === 0 ? (
        <EmptyResultsState />
      ) : (
        <ExpandableCardDemo cards={results as any} />
      )}
    </div>
  );
};

function useDebounce<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState<T>(value);
  useEffect(() => {
    const handle = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(handle);
  }, [value, delayMs]);
  return debounced;
}

export default ExplorePage;


