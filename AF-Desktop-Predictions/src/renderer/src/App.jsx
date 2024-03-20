import { useState, useEffect } from 'react'
import { api } from './Api'
import QueryInput from './components/QueryInput'
import QueuedPredictions from './components/QueuedPredictions'

function App() {
  // Todo: https://www.bugpilot.com/guides/en/building-a-chat-application-with-react-and-django-channels-0120
  // to show changes in the prediction state.
  const [queue, setQueue] = useState([])
  // Gracefully close socket on window close!
  const sigalsWebsocket = new WebSocket('ws://localhost:8000/ws/signals')

  sigalsWebsocket.onopen = () => {
    sigalsWebsocket.send(JSON.stringify({ name: 'Connection Established' }))
  }

  sigalsWebsocket.onmessage = (e) => {
    console.log(e.data)
  }

  const enqueuePrediction = () => {
    api.get('result').then((res) => {
      if (res.data.tasks != null && res.data.tasks.length >= 2) {
        console.log('Not executing shit since we have 2 predictions in queue already!')
      } else {
        api.post('trigger').then((res) => {
          // updateQueue()
        })
      }
    })
  }

  // const updateQueue = () => {
  //   api
  //     .get('/result')
  //     .then((res) => {
  //       if (res.data.tasks != null) {
  //         setQueue(res.data.tasks)
  //       } else {
  //         setQueue([]) // just in case
  //       }
  //     })
  //     .catch((err) => {
  //       console.log('Error occured!')
  //     })
  // }

  return (
    <div className="flex flex-col h-screen w-screen items-center bg-main-background">
      <header className="text-white font-bold text-2xl mt-5">LocalFold</header>
      <QueryInput />
      <button
        className="text-white bg-transparent mt-2 hover:text-gray-200"
        onClick={enqueuePrediction}
      >
        Queue Prediction
      </button>
      <QueuedPredictions queue={queue} />
    </div>
  )
}

export default App
