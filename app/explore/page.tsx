"use client";

import React, { useEffect, useMemo, useState } from 'react';
import ExpandableCardDemo from '@/components/expandable-card-demo-grid';
import Title from '@/components/title';
import { fetchYouTubeItems, MappedItem } from '@/lib/youtube';

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
    <div className='min-h-screen p-4 md:p-12 mt-20 max-w-7xl mx-auto'>
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

      <ExpandableCardDemo cards={results as any} />
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


