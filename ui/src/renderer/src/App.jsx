import { useState } from 'react'
import { signalsWebsocket, dataApi } from './Api'
import { Toaster, toast } from 'sonner'

import Setup from './components/Setup'
import QueuedPredictions from './components/QueuedPredictions'

const App = () => {
  // to show changes in the prediction state.
  const [queue, setQueue] = useState([])
  const [isConnected, setIsConnected] = useState(true)
  const [toggleSetup, setToggleSetup] = useState(false)

  const fetchTasks = () => {
    dataApi
      .get('/get-tasks')
      .then((response) => {
        if (response.status === 200) {
          setQueue(response.data.tasks)
        }
      })
      .catch(() => {
        toast.error('Error occured in fetching tasks!')
      })
  }

  window.electron.ipcRenderer.on('closing', () => {
    signalsWebsocket.close(1000) //  closing websocket connection as soon as window is closed!
  })

  signalsWebsocket.onerror = (e) => {
    setIsConnected(false)
  }

  signalsWebsocket.onopen = (e) => {
    // Fetch all tasks will add pagination later
    // as soon as the websocket is opened that means we are ready to
    // recieve updates therefore fetch tasks.
    fetchTasks()
  }

  signalsWebsocket.onclose = () => {
    toast.error('Disconnected!')
  }

  signalsWebsocket.onmessage = (message) => {
    // Recieve the task that has been updated
    // However we don't know how to change the queue directly yet
    // therefore fetching all the tasks again!
    var message = JSON.parse(message.data)
    fetchTasks()
  }

  const querySetup = () => {
    /*
     Handle query setup and trigger prediction
    */
    window.electron.ipcRenderer.send('query-selector')
    window.electron.ipcRenderer.on('query-selector-results', (_, msg) => {
      if (msg.filePath === undefined) return

      signalsWebsocket.send(
        JSON.stringify({
          execute: 'add_task',
          arg: msg.filePath[0]
        })
      )
    })
  }

  return (
    <div className="flex flex-col h-screen w-screen justify-center items-center bg-black">
      {isConnected ? (
        <>
          <header className="text-white font-bold text-2xl mt-5">LocalFold</header>
          {toggleSetup && <Setup toggleSetup={toggleSetup} setToggleSetup={setToggleSetup} />}
          <QueuedPredictions queue={queue} />
        </>
      ) : (
        <h1 className="text-center text-3xl font-bold text-red-600">Server offline!</h1>
      )}
      <nav className=" h-10 w-full flex justify-center">
        <button
          className="h-full mr-10 font-bold"
          onClick={() => {
            setToggleSetup(!toggleSetup)
          }}
        >
          Model Setup
        </button>
        <button
          className="h-full font-bold"
          onClick={() => {
            querySetup()
          }}
        >
          Select Query File
        </button>
      </nav>
      <Toaster />
    </div>
  )
}

export default App
