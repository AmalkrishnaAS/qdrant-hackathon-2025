import React from 'react'
import Image from 'next/image'
import { Separator } from '@/components/ui/separator'
import { items as defaultItems } from '@/app/data'
import ExpandableCardDemo from '@/components/expandable-card-demo-grid'
import Title from '@/components/title'
const index = async () => {
  return (
    <div
    className='min-h-screen p-4 md:p-12 mt-20 max-w-7xl mx-auto'
    >
     <Title
     title="Trending"
     description="Check out new releases"
     />
     <ExpandableCardDemo
     cards={defaultItems}
     />
    
     </div>
  )
}

export default index