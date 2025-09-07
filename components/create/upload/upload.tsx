'use client';

import { FileUpload } from '@/components/ui/file-upload';
import { useCreate } from '@/context/create-context';
import React, { useEffect } from 'react';
import { items as defaultItems } from '@/app/data';
import { List2 } from '@/components/ui/list';
import CTA from './cta';
import { Button } from '@/components/ui/button';
import { IconCheck, IconRefresh, IconUpload } from '@tabler/icons-react';
const Upload = () => {
  const { 
    items, 
    handleGetRecommendations, 
    isLoading,
    setActiveTab,
    files,
    selectedTrack,
    setSelectedTrack 
  } = useCreate();

  
  // Initialize items with default data
  // useEffect(() => {
  //   if (items.length === 0) {
  //     setItems(defaultItems);
  //   }
  // }, [items.length, setItems]);
  
  return (
    <div className="container mx-auto grid md:grid-cols-2 gap-8">
      
      <div className="flex items-center justify-center">
        <div className="w-full max-w-md flex items-center justify-center flex-col gap-5">
          <FileUpload />
          <div className='w-full flex items-center justify-center gap-2'>
          <Button
          disabled={items.length === 0}
          onClick={() => handleGetRecommendations(defaultItems)}
          variant="outline"
          className='flex-1'

          >Regenerate
          <IconRefresh className="ml-2 h-4 w-4" />
          </Button>
          <Button
          disabled={!selectedTrack}
          className='flex-1 '
          onClick={()=>setActiveTab('edit')}
          >Confirm
          <IconCheck className="ml-2 h-4 w-4" />
          </Button>
          </div>
          
        
        </div>
       
      </div>
      
      <div className="max-h-[55dvh] overflow-y-auto pr-4">
      {items.length > 0 && (
        <List2
          heading={`Recommended (${items.length})`}
          items={items}
          selectedTrackId={selectedTrack?.id || null}
          onSelectTrack={(track) => {
            setSelectedTrack(track);
          }}
        />
      )}
    {items.length === 0 && <CTA />}
      </div>
    </div>
  );
};

export default Upload;