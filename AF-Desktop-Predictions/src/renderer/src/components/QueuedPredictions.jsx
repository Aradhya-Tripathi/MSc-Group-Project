import { useEffect, useState } from 'react'
import { api } from '../Api'

const QueuedPredictions = ({ queue }) => {
  return (
    <div>
      {queue.map((item) => {
        return <h2 key={item.id}>{item.id}</h2>
      })}
    </div>
  )
}

export default QueuedPredictions
