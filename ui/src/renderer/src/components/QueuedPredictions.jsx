import TaskCard from './TaskCard'

const QueuedPredictions = ({ queue }) => {
  return (
    <div className="h-full w-[50%] overflow-auto bg-[#FAF9F6] rounded-lg">
      <h2 className="text-black text-center">Executing Predictions</h2>
      {Object.keys(queue).map((key, index) => {
        return <TaskCard taskId={key} taskStatus={queue[key]} key={index} />
      })}
    </div>
  )
}

export default QueuedPredictions
