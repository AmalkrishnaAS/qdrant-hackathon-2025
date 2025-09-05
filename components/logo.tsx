import React from 'react'
import Image from 'next/image'

const Logo = () => {
  return (
    <div
    className='fixed top-3 left-3'
    >
        <div
        className='flex items-center gap-2'
        >
        <Image
        src="/logo.svg"
        alt="Logo"
        width={40}
        height={40}
        />
        <h1
        className='text-xl font-semibold'
        >Reels2Vec</h1>
        </div>
    </div>
  )
}

export default Logo