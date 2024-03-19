import { useEffect, useState } from 'react'
import { api } from '../Api'

const QueuedPredictions = () => {
  const [queued, setQueued] = useState([])
  useEffect(() => {
    api
      .get('/result')
      .then((res) => {
        console.log(res.data.tasks)

        if (res.data.tasks != null) {
          setQueued(res.data.tasks)
        } else {
          setQueued([]) // just in case
        }
      })
      .catch((err) => {
        console.log('Error occured!')
      })
  }, [])
  return <div>QueuedPredictions</div>
}

export default QueuedPredictions
