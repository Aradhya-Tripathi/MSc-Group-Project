import { useEffect } from 'react'
import { api } from '../Api'

const QueuedPredictions = () => {
  useEffect(() => {
    api
      .get('/is-alive')
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.log('Error occured!')
      })
  }, [])
  return <div>QueuedPredictions</div>
}

export default QueuedPredictions
