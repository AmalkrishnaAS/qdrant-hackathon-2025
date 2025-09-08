'use client';

import { Button } from '@/components/ui/button';
import { Download, CheckCircle } from 'lucide-react';
import { useCreate } from '@/context/create-context';
import Image from 'next/image';

export default function DownloadTab() {
  const { selectedTrack } = useCreate();

  const handleDownload = () => {
    if (!selectedTrack) return;
    
    // Create a temporary anchor element
    const link = document.createElement('a');
    link.href = selectedTrack.audioUrl; // Assuming audioUrl exists on the track
    link.download = `${selectedTrack.title || 'track'}.mp3`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] p-6 text-center">
      <div className="max-w-md mx-auto space-y-6">
        <div className="flex justify-center">
        <Image
        src="/download.png"
        alt="Download"
        width={300}
        height={300}
        />
        </div>
        
        <h2 className="text-2xl font-bold tracking-tight">Your file is ready!</h2>
        <p className="text-muted-foreground">
          Your audio short video has been processed and is ready to download.
        </p>
        
        <div className="pt-4">
          <Button 
            onClick={handleDownload}
            size="lg"
            className="gap-2"
          >
            <Download className="h-4 w-4" />
            Download Track
          </Button>
        </div>
        
       
      </div>
    </div>
  );
}
