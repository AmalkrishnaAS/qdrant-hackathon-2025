'use client';
import React, { useEffect, useState } from 'react';

import { IconPlayerPlay, IconDotsVertical } from '@tabler/icons-react';
import { fetchYouTubeItems, MappedItem } from '@/lib/youtube';

interface Song extends MappedItem {
    addedDate: Date;
    isPlaying?: boolean;
}

export default function LibraryPage() {
    const [songs, setSongs] = useState<Song[]>([]);
    const [, setCurrentlyPlaying] = useState<string | null>(null);
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);

    // Fetch popular music from YouTube API
    useEffect(() => {
        const loadLibrarySongs = async () => {
            try {
                setLoading(true);
                const youtubeItems = await fetchYouTubeItems({
                    count: 20,
                    regionCode: 'US'
                });

                const songsWithDates: Song[] = youtubeItems.map((item, index) => ({
                    ...item,
                    addedDate: new Date(Date.now() - 86400000 * (index + 1)), // Simulate different add dates
                }));

                setSongs(songsWithDates);
            } catch (error) {
                console.error('Failed to load library songs:', error);
                // Fallback to empty array on error
                setSongs([]);
            } finally {
                setLoading(false);
            }
        };

        loadLibrarySongs();
    }, []);

    const filteredSongs = songs.filter(song =>
        song.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        song.artists.join(' ').toLowerCase().includes(searchQuery.toLowerCase()) ||
        song.album.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handlePlay = (song: Song) => {
        // Open YouTube video in new tab
        window.open(`https://www.youtube.com/watch?v=${song.videoId}`, '_blank');
        setCurrentlyPlaying(song.id);
    };

    const formatDate = (date: Date) => {
        const now = new Date();
        const diffTime = Math.abs(now.getTime() - date.getTime());
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 1) return 'Yesterday';
        if (diffDays < 7) return `${diffDays} days ago`;
        if (diffDays < 30) return `${Math.ceil(diffDays / 7)} weeks ago`;
        return date.toLocaleDateString();
    };

    return (
        <div className="p-4 md:p-12 mt-20 max-w-6xl mx-auto space-y-6 md:pb-16">
            <div>
                <h1 className="text-2xl font-semibold">Your Library</h1>
                <p className="text-sm text-muted-foreground">
                    {songs.length} songs in your collection
                </p>
            </div>

            {/* Search Bar */}
            <div className="relative">
                <input
                    type="text"
                    placeholder="Search songs, artists, or albums..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full px-4 py-2 bg-background border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20"
                />
            </div>

            {/* Library Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="p-4 rounded-lg border bg-card text-center">
                    <div className="text-2xl font-bold">{songs.length}</div>
                    <p className="text-sm text-muted-foreground">Total Songs</p>
                </div>
                <div className="p-4 rounded-lg border bg-card text-center">
                    <div className="text-2xl font-bold">
                        {new Set(songs.flatMap(s => s.artists)).size}
                    </div>
                    <p className="text-sm text-muted-foreground">Artists</p>
                </div>
                <div className="p-4 rounded-lg border bg-card text-center">
                    <div className="text-2xl font-bold">
                        {new Set(songs.map(s => s.album)).size}
                    </div>
                    <p className="text-sm text-muted-foreground">Albums</p>
                </div>
                <div className="p-4 rounded-lg border bg-card text-center">
                    <div className="text-2xl font-bold">
                        {Math.floor(songs.reduce((acc, song) => {
                            const [min, sec] = song.duration.split(':').map(Number);
                            return acc + min + sec / 60;
                        }, 0))}m
                    </div>
                    <p className="text-sm text-muted-foreground">Total Time</p>
                </div>
            </div>

            <div className="rounded-lg border bg-card text-card-foreground flex flex-col h-[600px]">
                {/* Header */}
                <div className="p-4 border-b flex-shrink-0">
                    <div className="grid grid-cols-12 gap-4 text-sm font-medium text-muted-foreground">
                        <div className="col-span-1">#</div>
                        <div className="col-span-5">Title</div>
                        <div className="col-span-3">Album</div>
                        <div className="col-span-2">Date Added</div>
                        <div className="col-span-1">Duration</div>
                    </div>
                </div>

                {/* Songs List */}
                <div className="divide-y overflow-y-auto flex-1">
                    {loading ? (
                        <div className="p-8 text-center text-muted-foreground">
                            Loading your library...
                        </div>
                    ) : filteredSongs.length === 0 ? (
                        <div className="p-8 text-center text-muted-foreground">
                            {searchQuery ? 'No songs match your search' : 'No songs in your library yet'}
                        </div>
                    ) : (
                        filteredSongs.map((song, index) => (
                            <div
                                key={song.id}
                                className="p-4 hover:bg-muted/50 transition-colors group"
                            >
                                <div className="grid grid-cols-12 gap-4 items-center">
                                    {/* Play Button / Index */}
                                    <div className="col-span-1">
                                        <div className="flex items-center justify-center w-8 h-8">
                                            <button
                                                onClick={() => handlePlay(song)}
                                                className="opacity-0 group-hover:opacity-100 transition-opacity hover:text-red-500"
                                                title="Play on YouTube"
                                            >
                                                <IconPlayerPlay className="w-4 h-4" />
                                            </button>
                                            <span className="group-hover:opacity-0 transition-opacity text-sm text-muted-foreground">
                                                {index + 1}
                                            </span>
                                        </div>
                                    </div>

                                    {/* Title & Artist */}
                                    <div className="col-span-5">
                                        <div className="flex items-center gap-3">
                                            <img
                                                src={song.thumbnails.default.url}
                                                alt={song.title}
                                                className="w-10 h-10 rounded object-cover"
                                            />
                                            <div>
                                                <div className="font-medium">{song.title}</div>
                                                <div className="text-sm text-muted-foreground">{song.artists.join(', ')}</div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Album / Channel */}
                                    <div className="col-span-3">
                                        <div className="text-sm text-muted-foreground">
                                            {song.album || song.artists[0] || 'YouTube'}
                                        </div>
                                    </div>

                                    {/* Date Added */}
                                    <div className="col-span-2">
                                        <div className="text-sm text-muted-foreground">
                                            {formatDate(song.addedDate)}
                                        </div>
                                    </div>

                                    {/* Duration */}
                                    <div className="col-span-1">
                                        <div className="flex items-center justify-between">
                                            <span className="text-sm text-muted-foreground">{song.duration}</span>
                                            <button className="opacity-0 group-hover:opacity-100 transition-opacity p-1 hover:bg-muted rounded">
                                                <IconDotsVertical className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}