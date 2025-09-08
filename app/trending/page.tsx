import React from 'react'
import Image from 'next/image'

import { fetchYouTubeItems } from '@/lib/youtube'
import ExpandableCardDemo from '@/components/expandable-card-demo-grid'
import Title from '@/components/title'
const index = async () => {
  const apiKey = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY
  let trending = []
  if (apiKey) {
    try {
      trending = await fetchYouTubeItems({ apiKey, count: 12 }) as any
    } catch (e) {
      // fall back to defaults on error
      trending = []
    }
  }
  return (
    <div
    className='min-h-screen p-4 md:p-12 mt-20 max-w-7xl mx-auto'
    >
     <Title
     title="Trending"
     description="Check out new releases"
     />
     <ExpandableCardDemo
     cards={trending as any}
     />
    
     </div>
  )
}

export default index