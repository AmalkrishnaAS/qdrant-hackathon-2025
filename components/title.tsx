import React from 'react'
const Title = ({title, description}: {title: string, description: string}) => {
  return (
    <div className='flex justify-center flex-col gap-1.5'>
      <h1 className='text-3xl font-semibold'>{title}</h1>
      <h2 className='text-lg text-muted-foreground'>{description}</h2>
      </div>    
        
  )

}

export default Title