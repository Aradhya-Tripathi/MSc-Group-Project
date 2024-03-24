const TaskCard = ({ taskId, taskStatus }) => {
  return (
    <div className="flex flex-col w-[100%] h-auto mt-2 overflow-scroll text-black border-black border-b-2">
      <h2 className="text-center">{taskId}</h2>
      <h2 className="text-center">{taskStatus}</h2>
    </div>
  )
}

export default TaskCard
