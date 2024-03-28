import TaskCard from './TaskCard'

const QueuedPredictions = ({ queue }) => {
  return (
    <div className="h-full w-[50%] overflow-auto bg-[#FAF9F6] rounded-lg">
      <h2 className="text-black text-center">Executing Predictions</h2>

      {queue.map((task) => {
        return (
          <TaskCard
            taskId={task.taskId}
            taskStatus={task.taskStatus}
            resultDestination={task.resultDestination}
            key={task.taskId}
          />
        )
      })}
    </div>
  )
}

export default QueuedPredictions
