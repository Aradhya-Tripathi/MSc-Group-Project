import QueryInput from './components/QueryInput'
import QueuedPredictions from './components/QueuedPredictions'

function App() {
  return (
    <div className="flex flex-col h-screen w-screen items-center bg-main-background">
      <header className="text-white text-2xl mt-5">Hello World!</header>
      <QueryInput />
      <button className="text-white bg-transparent mt-2">Enqueue</button>
      <QueuedPredictions />
    </div>
  )
}

export default App
