import React from 'react'
import {FileUpload} from '@/components/ui/file-upload'
import {List2} from '@/components/ui/list'
const Upload = ({items}: {items: any}) => {
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
    </div>
  </div>
  )
}

export default Upload