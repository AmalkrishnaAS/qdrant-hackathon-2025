'use client';
import React, { useEffect, useState, useCallback } from 'react';
import { Separator } from '@/components/ui/separator';

type TaskStatus = 'downloading' | 'vectorizing' | 'inserting' | 'completed' | 'failed';

interface IndexingTask {
  id: string;
  filename: string;
  status: TaskStatus;
  startTime: Date;
  endTime?: Date;
  error?: string;
}

type SSEMessage = {
  type: 'INIT' | 'UPDATE' | 'ADD';
  tasks?: IndexingTask[];
  task?: IndexingTask;
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<IndexingTask[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch initial tasks
  useEffect(() => {
    const fetchInitialTasks = async () => {
      try {
        const response = await fetch('/api/tasks');
        if (!response.ok) throw new Error('Failed to fetch tasks');
        const initialTasks = await response.json();
        setTasks(initialTasks.map(parseTaskDates));
      } catch (err) {
        setError('Failed to load tasks');
        console.error('Error fetching tasks:', err);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchInitialTasks();
  }, []);

  // Helper to parse date strings from the server
  const parseTaskDates = useCallback((task: any): IndexingTask => ({
    ...task,
    startTime: new Date(task.startTime),
    endTime: task.endTime ? new Date(task.endTime) : undefined,
  }), []);

  useEffect(() => {
    if (isLoading) return;

    const eventSource = new EventSource('/api/sse');

    eventSource.onopen = () => {
      console.log('SSE connection opened');
      setIsConnected(true);
      setError(null);
    };

    eventSource.onmessage = (event) => {
      try {
        const data: SSEMessage = JSON.parse(event.data);

        switch (data.type) {
          case 'INIT':
            if (data.tasks) {
              setTasks(data.tasks.map(parseTaskDates));
            }
            break;

          case 'ADD':
            if (data.task) {
              setTasks((prev) => [...prev, parseTaskDates(data.task!)]);
            }
            break;

          case 'UPDATE':
            if (data.task) {
              setTasks((prev) =>
                prev.map((task) =>
                  task.id === data.task?.id ? parseTaskDates(data.task!) : task
                )
              );
            }
            break;
        }
      } catch (err) {
        console.error('Error parsing SSE message:', err);
        setError('Error processing server updates');
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE error:', err);
      setError('Connection error. Please refresh the page to reconnect.');
      setIsConnected(false);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [parseTaskDates, isLoading]);

  const getConnectionStatus = () => {
    if (!isConnected) return 'Disconnected';
    return error ? 'Error' : 'Connected';
  };

  const getConnectionStatusColor = () => {
    if (!isConnected) return 'text-yellow-600 dark:text-yellow-400';
    return error ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400';
  };

  const getStatusColor = (status: TaskStatus) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 dark:text-green-400';
      case 'failed':
        return 'text-red-600 dark:text-red-400';
      case 'downloading':
      case 'vectorizing':
      case 'inserting':
        return 'text-blue-600 dark:text-blue-400';
      default:
        return 'text-yellow-600 dark:text-yellow-400';
    }
  };

  const getStatusText = (status: TaskStatus) => {
    switch (status) {
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      case 'downloading':
        return 'Downloading...';
      case 'vectorizing':
        return 'Vectorizing...';
      case 'inserting':
        return 'Inserting...';
      default:
        return 'Pending';
    }
  };

  const getStatusIcon = (status: TaskStatus) => {
    switch (status) {
      case 'completed':
        return '✓';
      case 'failed':
        return '✗';
      case 'downloading':
        return '↓';
      case 'vectorizing':
        return '▤';
      case 'inserting':
        return '↑';
      default:
        return '⏳';
    }
  };

  const isTaskInProgress = (status: TaskStatus) => {
    return ['downloading', 'vectorizing', 'inserting'].includes(status);
  };

  const formatDuration = (start: Date, end?: Date) => {
    const duration = (end || new Date()).getTime() - start.getTime();
    const seconds = Math.floor(duration / 1000);
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    return `${minutes}m ${seconds % 60}s`;
  };

  const activeTasks = tasks.filter((task) => isTaskInProgress(task.status));
  const completedTasks = tasks.filter((task) => !isTaskInProgress(task.status));

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
        <span className="ml-2">Loading tasks...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 text-center text-red-600">
        Error: {error}
      </div>
    );
  }

  return (
    <div className="p-4 md:p-12 mt-14 max-w-3xl mx-auto space-y-6">
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
            <div className="flex items-center space-x-2">
              <div className={`h-3 w-3 rounded-full ${getConnectionStatusColor()}`}></div>
              <span className="text-sm text-muted-foreground">
                {getConnectionStatus()}
              </span>
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
                      <span className={`text-lg ${getStatusColor(task.status)} ${isTaskInProgress(task.status) ? 'animate-pulse' : ''}`}>
                        {getStatusIcon(task.status)}
                      </span>
                      <div className="min-w-0">
                        <div className="font-medium truncate">{task.filename}</div>
                        <div className={`text-xs ${getStatusColor(task.status)}`}>
                          {getStatusText(task.status)}
                        </div>
                      </div>
                    </div>
                    <div className="text-xs text-muted-foreground whitespace-nowrap ml-2">
                      {formatDuration(task.startTime, task.endTime)}
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