import React from 'react';
import { FileUpload } from '@/components/ui/file-upload';
import { List2 } from '@/components/ui/list';
import { useCreate } from '@/context/create-context';

const Upload = ({ items }: { items: any }) => {
  const { files } = useCreate();
  
  return (
    <div className="container mx-auto grid md:grid-cols-2 gap-8">
      <div className="flex items-center justify-center">
        <div className="w-full max-w-md">
          <FileUpload />
        </div>
      </div>
      <div className="max-h-[55dvh] overflow-y-auto pr-4">
        <List2
          heading={`Recommended Tracks (${items.length})`}
          items={items}
        />
        {files.length > 0 && (
          <div className="mt-4">
            <h3 className="text-lg font-medium mb-2">Uploaded Files ({files.length})</h3>
            <ul className="space-y-2">
              {files.map((file, index) => (
                <li key={index} className="text-sm text-gray-600 dark:text-gray-300">
                  {file.name}
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Upload;