import TaskCard from './TaskCard'

const QueuedPredictions = ({ queue }) => {
  return (
    <div className="h-full overflow-auto">
      {Object.keys(queue).map((key, index) => {
        return <TaskCard taskId={key} taskStatus={queue[key]} />
      })}
    </div>
  )
}

export default QueuedPredictions
