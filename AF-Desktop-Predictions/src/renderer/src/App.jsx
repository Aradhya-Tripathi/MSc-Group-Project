import { api } from './Api'
import QueryInput from './components/QueryInput'
import QueuedPredictions from './components/QueuedPredictions'

function App() {
  const enqueuePrediction = () => {
    api.get('result').then((res) => {
      if (res.data.tasks != null && res.data.tasks.length >= 2) {
        console.log('Not executing shit since we have 2 predictions in queue already!')
      } else {
        api.post('trigger').then((res) => {
          console.log(res.data) // Queue Id
        })
      }
    })
  }

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
      <QueuedPredictions />
    </div>
  )
}

export default App
