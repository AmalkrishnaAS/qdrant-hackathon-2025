import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { useCreate } from '@/context/create-context';
import { items as defaultItems } from '@/app/data';

const GridPattern = () => (
    <div className="absolute inset-0">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,var(--tw-gradient-stops))] from-background/0 via-background/30 to-background/80 dark:from-background/0 dark:via-background/40 dark:to-background/90" />
      <svg
        className="absolute inset-0 h-full w-full opacity-70"
        fill="none"
      >
        <defs>
          <pattern
            id="pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8a"
            x="0"
            y="0"
            width="40"
            height="40"
            patternUnits="userSpaceOnUse"
            patternTransform="scale(1) translate(0 0)"
          >
            <rect
              x="0"
              y="0"
              width="40"
              height="40"
              className="fill-background/0"
            />
            <path
              d="M0 40L40 0"
              className="stroke-muted/40"
              strokeWidth="1"
            />
          </pattern>
          <radialGradient id="grid-fade" cx="50%" cy="50%" r="70%" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="var(--background)" stopOpacity="0" />
            <stop offset="100%" stopColor="var(--background)" stopOpacity="0.9" />
          </radialGradient>
        </defs>
        <rect
          width="100%"
          height="100%"
          strokeWidth="0"
          fill="url(#pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8a)"
        />
        <rect width="100%" height="100%" fill="url(#grid-fade)" />
      </svg>
    </div>
  );
const CTA = () => {
  const { handleGetRecommendations, isLoading, files } = useCreate();
  
  const handleClick = async () => {
    try {
      await handleGetRecommendations(defaultItems);
    } catch (error) {
      // Error is already logged in the context
      // You could add additional error handling here if needed
    }
  };

  return (
    <div className="h-[55dvh]">
    <div className="relative flex flex-col items-center justify-center p-8 border-2 border-dashed border-border rounded-lg text-center h-full bg-card overflow-hidden">
      <GridPattern />
      <div className="relative space-y-4 z-10 bg-background/80 dark:bg-background/90 backdrop-blur-sm p-6 rounded-lg border border-border/50">
        <h3 className="text-lg font-medium text-foreground">No recommendations yet</h3>
        <p className="text-sm text-muted-foreground">Upload a file or enter a URL to get started</p>
        <Button 
          onClick={handleClick}
          className="mt-4 min-w-[180px] h-10"
          disabled={isLoading || files.length === 0}
        >
          <span className="inline-flex items-center justify-center w-full">
            {isLoading ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Loading...
              </>
            ) : (
              'Get Recommendations'
            )}
          </span>
        </Button>
      </div>
    </div>
    </div>
  );
};

export default CTA;