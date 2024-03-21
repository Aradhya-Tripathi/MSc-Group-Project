import { useState } from 'react'
import { signalsWebsocket } from './Api'
import QueryInput from './components/QueryInput'
import QueuedPredictions from './components/QueuedPredictions'

function App() {
  // Todo: https://www.bugpilot.com/guides/en/building-a-chat-application-with-react-and-django-channels-0120
  // to show changes in the prediction state.
  const [queue, setQueue] = useState({})
  const [isConnected, setIsConnected] = useState(true)
  // Gracefully close socket on window close!
  // We are connected at this point!

  signalsWebsocket.onerror = (e) => {
    setIsConnected(false)
  }

  signalsWebsocket.onopen = (e) => {
    console.log('Socket opened!')
  }

  signalsWebsocket.onmessage = (e) => {
    // Set the queue accordingly
    setQueue(JSON.parse(e.data).tasks)
  }

  const enqueuePrediction = () => {
    signalsWebsocket.send(
      JSON.stringify({
        execute: 'add_task'
      })
    )
  }

  return (
    <div className="flex flex-col h-screen w-screen justify-center items-center bg-main-background">
      {isConnected ? (
        <>
          <header className="text-white font-bold text-2xl mt-5">LocalFold</header>
          <QueryInput />
          <button
            className="text-white bg-transparent mt-2 hover:text-gray-200"
            onClick={enqueuePrediction}
          >
            Queue Prediction
          </button>
          <QueuedPredictions queue={queue} />
        </>
      ) : (
        <h1 className="text-center text-3xl font-bold text-red-600">Server offline!</h1>
      )}
    </div>
  )
}

export default App
