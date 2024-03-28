const TaskCard = ({ taskId, taskStatus, resultDestination }) => {
  let backgroundColorClass = ''

  switch (taskStatus) {
    case 'successful':
      backgroundColorClass = 'bg-green-200'
      break
    case 'running':
      backgroundColorClass = 'bg-yellow-200'
      break
    default:
      backgroundColorClass = 'bg-gray-200'
  }

  return (
    <div
      className={`flex flex-col w-[100%] h-auto mt-2 overflow-scroll text-black border-black border-b-2 hover:cursor-pointer ${backgroundColorClass}`}
      onClick={() => {
        window.electron.ipcRenderer.send('clicked-prediction', {
          taskId: taskId,
          resultDestination: resultDestination
        })
      }}
    >
      <h2 className="text-center">{taskId}</h2>
      <h2 className="text-center">{taskStatus}</h2>
    </div>
  )
}

export default TaskCard
