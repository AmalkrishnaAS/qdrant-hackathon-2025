import React from 'react'
import { Separator } from '@/components/ui/separator'

const index = () => {
  return (
    <div
    className='min-h-screen p-4 md:p-12 mt-20 max-w-8xl mx-auto'
    >
      <div className='flex justify-center flex-col gap-1.5 '>
      <h1 className='text-3xl font-semibold'>Trending</h1>
      <h2 className='text-lg text-muted-foreground'>Check out new releases</h2>
      </div>
    </div>
  )
}

export default index