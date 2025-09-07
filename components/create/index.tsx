"use client"
import React from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { IconChevronRight } from "@tabler/icons-react"
import Upload from "./upload"
import { AudioVideoSplitter } from "./edit"
import { items } from "@/app/data"
import { CreateProvider, useCreate } from "@/context/create-context"

const CreateTabs = () => {
  const { activeTab, setActiveTab } = useCreate()

  return (
    <Tabs 
      value={activeTab} 
      onValueChange={setActiveTab}
      className="w-full"
    >
      <TabsList className="grid w-full grid-cols-3 max-w-lg mx-auto">
        <TabsTrigger value="upload" className="flex items-center gap-1">
          Upload <IconChevronRight className="h-4 w-4" />
        </TabsTrigger>
        <TabsTrigger value="edit" className="flex items-center gap-1">
          Edit <IconChevronRight className="h-4 w-4" />
        </TabsTrigger>
        <TabsTrigger value="download" className="flex items-center gap-1">
          Download <IconChevronRight className="h-4 w-4" />
        </TabsTrigger>
      </TabsList>
      <TabsContent value="upload" className="mt-6">
        <Upload items={items} />
      </TabsContent>
      <TabsContent value="edit" className="mt-6">
        <AudioVideoSplitter videoUrl="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4" />
      </TabsContent>
      <TabsContent value="download" className="mt-6">
        <div className="text-center py-8">
          <h3 className="text-lg font-medium">Download Content</h3>
          <p className="text-muted-foreground mt-2">Download your files here</p>
        </div>
      </TabsContent>
    </Tabs>
  )
}

const Create = () => {
  return (
    <CreateProvider>
      <CreateTabs />
    </CreateProvider>
  )
}

export default Create