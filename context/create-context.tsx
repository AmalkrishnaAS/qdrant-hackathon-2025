'use client'

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface CreateContextType {
  // Tab state
  activeTab: string;
  setActiveTab: (tab: string) => void;
  
  // Files state
  files: File[];
  addFiles: (newFiles: File[]) => void;
  removeFile: (index: number) => void;
  clearFiles: () => void;
}

const CreateContext = createContext<CreateContextType | undefined>(undefined);

export const CreateProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState<string>('upload');
  const [files, setFiles] = useState<File[]>([]);

  const addFiles = (newFiles: File[]) => {
    setFiles(prevFiles => [...prevFiles, ...newFiles]);
  };

  const removeFile = (index: number) => {
    setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
  };

  const clearFiles = () => {
    setFiles([]);
  };

  const value = {
    activeTab,
    setActiveTab,
    files,
    addFiles,
    removeFile,
    clearFiles
  };

  return (
    <CreateContext.Provider value={value}>
      {children}
    </CreateContext.Provider>
  );
};

export const useCreate = () => {
  const context = useContext(CreateContext);
  if (context === undefined) {
    throw new Error('useCreate must be used within a CreateProvider');
  }
  return context;
};
