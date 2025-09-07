
  import React from "react";
  
  import { Button } from "@/components/ui/button";
  import { Separator } from "@/components/ui/separator";
import { IconPlayerPlay, IconPlayerPlayFilled } from "@tabler/icons-react";
  
  interface Thumbnail {
    url: string;
    width: number;
    height: number;
  }

  interface ListItem {
    id: string;
    title: string;
    artists: string[];
    album: string;
    duration: string;
    thumbnails: {
      default: Thumbnail;
      medium: Thumbnail;
      high: Thumbnail;
    };
    videoId: string;
    isExplicit: boolean;
    category: string;
    description: string;
  }
  
  interface List2Props {
    heading?: string;
    items?: ListItem[];
    onSelectTrack?: (track: ListItem) => void;
    selectedTrackId?: string | null;
  }
  
  const List2 = ({
    heading,
    items=[],
    onSelectTrack,
    selectedTrackId = null,
  }: List2Props) => {
    return (
      <section className="py-4">
        <div className="container px-0">
          <h1 className="mb-6 px-4 text-2xl font-semibold md:text-3xl">
            {heading}
          </h1>
          <div className="flex flex-col ">
            <Separator />
            {items.map((item, index) => (
              <React.Fragment key={index}>
                <div className="grid items-center gap-3 px-3 py-3 hover:bg-muted/50 transition-colors rounded-lg grid-cols-1 md:grid-cols-2">
                  <div className="flex items-center gap-3">
                    <img
                      src={item.thumbnails.default.url}
                      alt={item.title}
                      className="h-12 w-12 rounded-md object-cover flex-shrink-0"
                    />
                    <div className="flex-1 min-w-0">
                      <h3 className="font-semibold truncate">{item.title}</h3>
                      <p className="text-sm text-muted-foreground truncate">
                        {item.album}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center justify-end gap-2 mt-2 md:mt-0">
                    <Button 
                      variant="outline" 
                      size="sm" 
                      className="h-8 px-3 text-xs"
                      onClick={(e) => {
                        e.stopPropagation();
                        window.open(`https://music.youtube.com/watch?v=${item.videoId}`, '_blank');
                      }}
                    >
                      <svg className="w-4 h-4 mr-1.5" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0C5.376 0 0 5.376 0 12s5.376 12 12 12 12-5.376 12-12S18.624 0 12 0zm5.04 15.6c-.12.24-.36.36-.6.36h-1.2c-.24 0-.48-.12-.6-.36l-1.2-2.4-1.2 2.4c-.12.24-.36.36-.6.36H7.56c-.24 0-.48-.12-.6-.36l-1.2-2.4-1.2 2.4c-.12.24-.36.36-.6.36H2.76c-.24 0-.48-.12-.6-.36l3.6-7.2c.12-.24.36-.36.6-.36h1.2c.24 0 .48.12.6.36l1.2 2.4 1.2-2.4c.12-.24.36-.36.6-.36h1.2c.24 0 .48.12.6.36l3.6 7.2z"/>
                      </svg>
                      Listen
                    </Button>
                    <Button 
                      variant={selectedTrackId === item.id ? 'default' : 'outline'}
                      size="sm" 
                      className="h-8 px-3 text-xs"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (onSelectTrack) {
                          onSelectTrack(item);
                        }
                      }}
                    >
                      <IconPlayerPlayFilled className="w-4 h-4 mr-1.5" />
                      {selectedTrackId === item.id ? 'Selected' : 'Select'}
                    </Button>
                  </div>
                </div>
                <Separator />
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>
    );
  };
  
  export { List2 };
  