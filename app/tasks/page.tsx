'use client';
import React, { useEffect, useState } from 'react';
import { Separator } from '@/components/ui/separator';

interface IndexingTask {
  id: string;
  filename: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  startTime: Date;
  endTime?: Date;
  error?: string;
}

export default function TasksPage() {
  const [tasks, setTasks] = useState<IndexingTask[]>([]);
  const [isPolling, setIsPolling] = useState(true);

  // Mock data for demonstration
  useEffect(() => {
    const mockTasks: IndexingTask[] = [
      {
        id: '1',
        filename: 'Song Title - Artist Name.mp3',
        status: 'completed',
        startTime: new Date(Date.now() - 120000),
        endTime: new Date(Date.now() - 60000),
      },
      {
        id: '2',
        filename: 'Another Song - Different Artist.mp3',
        status: 'processing',
        startTime: new Date(Date.now() - 30000),
      },
      {
        id: '3',
        filename: 'Third Track - Band Name.mp3',
        status: 'pending',
        startTime: new Date(),
      },
    ];
    setTasks(mockTasks);
  }, []);

  const getStatusColor = (status: IndexingTask['status']) => {
    switch (status) {
      case 'completed': return 'text-green-600 dark:text-green-400';
      case 'processing': return 'text-blue-600 dark:text-blue-400';
      case 'pending': return 'text-yellow-600 dark:text-yellow-400';
      case 'failed': return 'text-red-600 dark:text-red-400';
      default: return 'text-muted-foreground';
    }
  };

  const getStatusIcon = (status: IndexingTask['status']) => {
    switch (status) {
      case 'completed': return '✓';
      case 'processing': return '⟳';
      case 'pending': return '⏳';
      case 'failed': return '✗';
      default: return '?';
    }
  };

  const getStatusText = (status: IndexingTask['status']) => {
    switch (status) {
      case 'completed': return 'Indexed';
      case 'processing': return 'Vectorizing...';
      case 'pending': return 'Queued';
      case 'failed': return 'Failed';
      default: return 'Unknown';
    }
  };

  const formatDuration = (start: Date, end?: Date) => {
    const duration = (end || new Date()).getTime() - start.getTime();
    const seconds = Math.floor(duration / 1000);
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m ${seconds % 60}s`;
  };

  const activeTasks = tasks.filter(t => t.status === 'processing' || t.status === 'pending');
  const completedTasks = tasks.filter(t => t.status === 'completed' || t.status === 'failed');

  return (
    <div className=" p-4 md:p-12 mt-20 max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Indexing Tasks</h1>
        <p className="text-sm text-muted-foreground">Track the progress of song vectorization and indexing</p>
      </div>

      <div className="divide-y rounded-lg border bg-card text-card-foreground">
        {/* Status Overview */}
        <div className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-medium">Status Overview</h2>
              <p className="text-xs text-muted-foreground">Current indexing activity</p>
            </div>
            <div className="flex items-center gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full ${isPolling ? 'bg-green-500 animate-pulse' : 'bg-muted-foreground'}`} />
                <span className="text-muted-foreground">
                  {isPolling ? 'Live updates' : 'Paused'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Active Tasks */}
        {activeTasks.length > 0 && (
          <>
            <Separator />
            <div className="p-4">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-base font-medium">Active Tasks</h2>
                  <p className="text-xs text-muted-foreground">{activeTasks.length} songs being processed</p>
                </div>
              </div>
              <div className="space-y-3">
                {activeTasks.map((task) => (
                  <div key={task.id} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className={`text-lg ${getStatusColor(task.status)} ${task.status === 'processing' ? 'animate-spin' : ''}`}>
                        {getStatusIcon(task.status)}
                      </span>
                      <div>
                        <div className="font-medium">{task.filename}</div>
                        <div className={`text-xs ${getStatusColor(task.status)}`}>
                          {getStatusText(task.status)}
                        </div>
                      </div>
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {formatDuration(task.startTime)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Recent Tasks */}
        <Separator />
        <div className="p-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-medium">Recent Tasks</h2>
              <p className="text-xs text-muted-foreground">{completedTasks.length} completed or failed</p>
            </div>
          </div>
          {completedTasks.length === 0 ? (
            <p className="text-muted-foreground text-center py-4 text-sm">
              No completed tasks yet
            </p>
          ) : (
            <div className="space-y-3">
              {completedTasks.slice(0, 5).map((task) => (
                <div key={task.id} className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className={`text-lg ${getStatusColor(task.status)}`}>
                      {getStatusIcon(task.status)}
                    </span>
                    <div>
                      <div className="font-medium">{task.filename}</div>
                      <div className={`text-xs ${getStatusColor(task.status)}`}>
                        {getStatusText(task.status)}
                      </div>
                    </div>
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {formatDuration(task.startTime, task.endTime)}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Summary Stats */}
        <Separator />
        <div className="p-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-base font-medium">Statistics</h2>
              <p className="text-xs text-muted-foreground">Task summary</p>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-xl font-bold">{tasks.length}</div>
              <p className="text-xs text-muted-foreground">Total</p>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-blue-600">{activeTasks.length}</div>
              <p className="text-xs text-muted-foreground">Active</p>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-green-600">
                {tasks.filter(t => t.status === 'completed').length}
              </div>
              <p className="text-xs text-muted-foreground">Completed</p>
            </div>
            <div className="text-center">
              <div className="text-xl font-bold text-red-600">
                {tasks.filter(t => t.status === 'failed').length}
              </div>
              <p className="text-xs text-muted-foreground">Failed</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}