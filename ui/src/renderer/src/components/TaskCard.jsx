const TaskCard = ({ taskId, taskStatus }) => {
  return (
    <div className="bg-black flex flex-col w-[100%] h-auto mt-2 overflow-scroll">
      <h2>{taskId}</h2>
      <h2 className="text-center">{taskStatus}</h2>
    </div>
  )
}

export default TaskCard
