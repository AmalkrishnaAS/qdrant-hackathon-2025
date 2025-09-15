import { NextResponse } from 'next/server';

type TaskStatus = 'downloading' | 'vectorizing' | 'inserting' | 'completed' | 'failed';

interface Task {
  id: string;
  filename: string;
  status: TaskStatus;
  startTime: string;
  endTime?: string;
  error?: string;
}

// Mock data - in a real app, this would come from a database
const ALL_TASKS: Omit<Task, 'startTime' | 'status'>[] = [
  { id: '1', filename: 'Bohemian Rhapsody - Queen.mp3' },
  { id: '2', filename: 'Stairway to Heaven - Led Zeppelin.mp3' },
  { id: '3', filename: 'Hotel California - Eagles.mp3' },
  { id: '4', filename: 'Sweet Child O\'Mine - Guns N\' Roses.mp3' },
  { id: '5', filename: 'Smells Like Teen Spirit - Nirvana.mp3' },
  { id: '6', filename: 'Imagine - John Lennon.mp3' },
  { id: '7', filename: 'Billie Jean - Michael Jackson.mp3' },
  { id: '8', filename: 'Like a Rolling Stone - Bob Dylan.mp3' },
  { id: '9', filename: 'I Will Always Love You - Whitney Houston.mp3' },
  { id: '10', filename: 'Hey Jude - The Beatles.mp3' },
];

// Helper to generate random status based on task age
function getRandomStatus(startTime: Date): TaskStatus {
  const now = new Date();
  const ageInMinutes = (now.getTime() - startTime.getTime()) / (1000 * 60);
  
  if (ageInMinutes > 5) {
    return Math.random() > 0.2 ? 'completed' : 'failed';
  }
  
  const statuses: TaskStatus[] = ['downloading', 'vectorizing', 'inserting'];
  const statusIndex = Math.min(
    Math.floor(ageInMinutes / 2), // Progress status based on age
    statuses.length - 1
  );
  
  return statuses[statusIndex];
}

export async function GET() {
  try {
    // Select 5 random tasks
    const selectedTasks = [...ALL_TASKS]
      .sort(() => 0.5 - Math.random())
      .slice(0, 5)
      .map(task => {
        const startTime = new Date();
        startTime.setMinutes(startTime.getMinutes() - Math.floor(Math.random() * 10)); // Random start time in last 10 minutes
        
        const status = getRandomStatus(startTime);
        const taskWithStatus: Task = {
          ...task,
          status,
          startTime: startTime.toISOString(),
        };
        
        if (status === 'completed' || status === 'failed') {
          const endTime = new Date(startTime);
          endTime.setSeconds(endTime.getSeconds() + Math.floor(Math.random() * 30) + 10); // Random duration 10-40s
          taskWithStatus.endTime = endTime.toISOString();
          
          if (status === 'failed') {
            taskWithStatus.error = Math.random() > 0.5 
              ? 'Network error during download' 
              : 'Vectorization failed';
          }
        }
        
        return taskWithStatus;
      });

    return NextResponse.json(selectedTasks);
  } catch (error) {
    console.error('Error fetching tasks:', error);
    return new NextResponse('Internal Server Error', { status: 500 });
  }
}
