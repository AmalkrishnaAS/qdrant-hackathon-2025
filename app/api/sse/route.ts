import { NextResponse } from 'next/server';

type TaskStatus = 'downloading' | 'vectorizing' | 'inserting' | 'completed' | 'failed';

interface IndexingTask {
  id: string;
  filename: string;
  status: TaskStatus;
  startTime: string;
  endTime?: string;
  error?: string;
}

// Get the next status in sequence
function getNextStatus(currentStatus: TaskStatus): TaskStatus {
  const statusOrder: TaskStatus[] = ['downloading', 'vectorizing', 'inserting', 'completed'];
  const currentIndex = statusOrder.indexOf(currentStatus);
  return currentIndex < statusOrder.length - 1 
    ? statusOrder[currentIndex + 1] 
    : currentStatus;
}

export async function GET() {
  try {
    // Fetch initial tasks
    const response = await fetch(`${process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000'}/api/tasks`);
    if (!response.ok) throw new Error('Failed to fetch tasks');
    
    const encoder = new TextEncoder();
    let tasks: IndexingTask[] = await response.json();
    
    return new NextResponse(
      new ReadableStream({
        async start(controller) {
          // Send initial tasks
          controller.enqueue(encoder.encode(`data: ${JSON.stringify({ 
            type: 'INIT', 
            tasks 
          })}\n\n`));

          // Update tasks
          const updateInterval = setInterval(() => {
            tasks = tasks.map(task => {
              if (task.status === 'completed' || task.status === 'failed') {
                return task;
              }
              
              const shouldUpdate = Math.random() > 0.7;
              if (!shouldUpdate) return task;
              
              const nextStatus = getNextStatus(task.status);
              const updatedTask = {
                ...task,
                status: nextStatus,
                ...(nextStatus === 'completed' || nextStatus === 'failed' ? { 
                  endTime: new Date().toISOString() 
                } : {})
              };
              
              if (nextStatus === 'failed' && !updatedTask.error) {
                updatedTask.error = Math.random() > 0.5 
                  ? 'Network error' 
                  : 'Processing failed';
              }
              
              controller.enqueue(encoder.encode(`data: ${JSON.stringify({
                type: 'UPDATE',
                task: updatedTask
              })}\n\n`));
              
              return updatedTask;
            });
          }, 2000);

          return () => clearInterval(updateInterval);
        },
      }),
      {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      }
    );
  } catch (error) {
    console.error('SSE Error:', error);
    return new NextResponse('SSE Error', { status: 500 });
  }
}
