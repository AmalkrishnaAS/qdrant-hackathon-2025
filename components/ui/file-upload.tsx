"use client";

import { cn } from "@/lib/utils";
import { useRef } from "react";
import { IconUpload, IconX } from "@tabler/icons-react";
import { useDropzone } from "react-dropzone";
import { useCreate } from "@/context/create-context";

export const FileUpload = () => {
  const { files, addFiles, removeFile } = useCreate();
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (newFiles: File[]) => {
    addFiles(newFiles);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const { getRootProps, isDragActive } = useDropzone({
    multiple: false,
    noClick: true,
    accept: {
      'video/*': []
    },
    onDrop: handleFileChange,
    onDropRejected: (rejections) => {
      console.log('Rejected files:', rejections);
      // You can add user feedback here if needed
    },
    maxFiles: 1
  });

  return (
    <div className="w-full" {...getRootProps()}>
      <div
        onClick={handleClick}
        className="p-6 group/file block rounded-lg cursor-pointer w-full relative overflow-hidden border-2 border-dashed border-gray-300 dark:border-gray-700 hover:border-blue-500 transition-colors"
      >
        <input
          ref={fileInputRef}
          id="file-upload-handle"
          type="file"
          accept="video/*"
          onChange={(e) => {
            const files = e.target.files ? Array.from(e.target.files) : [];
            const videoFiles = files.filter(file => file.type.startsWith('video/'));
            handleFileChange(videoFiles);
          }}
          className="hidden"
        />
        <div className="absolute inset-0 [mask-image:radial-gradient(ellipse_at_center,white,transparent)]">
          <GridPattern />
        </div>
        <div className="flex flex-col items-center justify-start relative z-10 h-full">
          <div className="text-center">
            <p className="font-sans font-bold text-neutral-700 dark:text-neutral-300 text-base mb-1">
              Upload Video
            </p>
            <p className="text-xs text-muted-foreground">MP4, WebM, MOV, etc.</p>
          </div>
          <p className="text-center font-sans font-normal text-neutral-400 dark:text-neutral-400 text-sm mb-4">
            Drag & drop your files here or click to browse
          </p>
          
          <div className="w-full flex-1 flex flex-col min-h-[200px] max-h-[400px] overflow-y-auto">
            {files.length === 0 ? (
              <div className={cn(
                "relative flex-1 flex items-center justify-center w-full rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 transition-colors",
                isDragActive ? "border-blue-400 bg-blue-50/50 dark:bg-blue-900/20" : "hover:border-blue-400 hover:bg-gray-50/50 dark:hover:bg-neutral-800/50",
                "shadow-[0px_4px_20px_rgba(0,0,0,0.08)] h-full min-h-[180px]"
              )}>
                <div className="flex flex-col items-center p-4 text-center">
                  {isDragActive ? (
                    <>
                      <IconUpload className="h-7 w-7 text-blue-500 mb-2" />
                      <p className="text-sm font-medium text-blue-600 dark:text-blue-400">Drop your files here</p>
                      <p className="text-xs text-blue-500 dark:text-blue-300 mt-1">We'll take care of the rest</p>
                    </>
                  ) : (
                    <>
                      <IconUpload className="h-7 w-7 text-neutral-400 dark:text-neutral-500 mb-2" />
                      <p className="text-sm font-medium text-neutral-700 dark:text-neutral-300">Drag & drop files here</p>
                      <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">or click to browse files</p>
                    </>
                  )}
                </div>
              </div>
            ) : (
              <div className="space-y-2 pr-2">
                {files.map((file, idx) => (
                  <div
                    key={idx}
                    className="relative z-40 bg-white dark:bg-neutral-800 flex items-center justify-between p-3 rounded-md shadow-sm border border-gray-100 dark:border-neutral-700"
                  >
                    <p className="text-sm text-neutral-700 dark:text-neutral-300 truncate max-w-[70%]">
                      {file.name}
                    </p>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFile(idx);
                      }}
                      className="text-red-500 hover:text-red-600 p-1.5 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                      aria-label="Remove file"
                    >
                      <IconX className="h-3.5 w-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const GridPattern = () => (
  <svg
    className="absolute inset-0 h-full w-full stroke-neutral-200 dark:stroke-neutral-700"
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
          className="fill-neutral-100 dark:fill-neutral-900"
        />
        <path
          d="M0 40L40 0"
          className="stroke-neutral-200 dark:stroke-neutral-800"
          strokeWidth="1"
        />
      </pattern>
    </defs>
    <rect
      width="100%"
      height="100%"
      strokeWidth="0"
      fill="url(#pattern-5c1e4f0e-62d5-498b-8ff0-cf77bb448c8a)"
    />
  </svg>
);
