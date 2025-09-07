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
  
  // Track items state
  items: any[];
  setItems: (items: any[]) => void;
  selectedTrack: any | null;
  setSelectedTrack: (track: any | null) => void;
  
  // Recommendations
  isLoading: boolean;
  handleGetRecommendations: (defaultItems: any[]) => Promise<void>;
}

const CreateContext = createContext<CreateContextType | undefined>(undefined);

export const CreateProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState<string>('upload');
  const [files, setFiles] = useState<File[]>([]);
  const [items, setItems] = useState<any[]>([]);
  const [selectedTrack, setSelectedTrack] = useState<any | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const addFiles = (newFiles: File[]) => {
    setFiles(prevFiles => [...prevFiles, ...newFiles]);
  };

  const removeFile = (index: number) => {
    setFiles(prevFiles => prevFiles.filter((_, i) => i !== index));
  };

  const clearFiles = () => {
    setFiles([]);
  };

  const handleGetRecommendations = async (defaultItems: any[]) => {
    try {
      setIsLoading(true);
      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 800));
      
      // Set the items from provided defaultItems
      setItems([...defaultItems]);
    } catch (error) {
      console.error('Failed to fetch recommendations:', error);
      // You could add error handling here, like showing a toast notification
      throw error; // Re-throw to allow component-level error handling
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    activeTab,
    setActiveTab,
    files,
    addFiles,
    removeFile,
    clearFiles,
    items,
    setItems,
    selectedTrack,
    setSelectedTrack,
    isLoading,
    handleGetRecommendations
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
