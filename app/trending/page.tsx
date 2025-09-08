import React from 'react'
import Image from 'next/image'

import { fetchYouTubeItems } from '@/lib/youtube'
import ExpandableCardDemo from '@/components/expandable-card-demo-grid'
import Title from '@/components/title'
import { cookies } from 'next/headers'
import { formatRegionLabel } from '@/lib/regions'
const index = async () => {
  const apiKey = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY
  const cookieStore = await cookies()
  const region = cookieStore.get('trending_region')?.value || 'US'
  const countCookie = cookieStore.get('trending_count')?.value
  const count = countCookie ? Math.max(1, Math.min(50, parseInt(countCookie, 10) || 12)) : 12
  let trending = []
  if (apiKey) {
    try {
      trending = await fetchYouTubeItems({ apiKey, count, regionCode: region }) as any
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
     description={`Showing ${count} trends for ${formatRegionLabel(region)}`}
     />
     <ExpandableCardDemo
     cards={trending as any}
     />
    
     </div>
  )
}

export default index