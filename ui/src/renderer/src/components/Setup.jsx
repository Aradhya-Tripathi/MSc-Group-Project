import { signalsWebsocket } from '../Api'
import { toast } from 'sonner'

const Setup = ({ toggleSetup, setToggleSetup }) => {
  let setup = { modelType: 'auto' }

  const modelParametersSetup = () => {
    window.electron.ipcRenderer.send('model-selector')
    window.electron.ipcRenderer.on('model-selector-results', (_, msg) => {
      if (msg.filePath === undefined) return
      setup.modelPath = msg.filePath[0]
    })
  }

  const resultDirSetup = () => {
    window.electron.ipcRenderer.send('results-dir-selector')
    window.electron.ipcRenderer.on('results-dir-results', (_, msg) => {
      if (msg.filePath === undefined) return
      setup.resultPath = msg.filePath[0]
    })
  }

  return (
    <div className="h-screen w-screen absolute bg-black flex flex-col items-center">
      <header className="text-white font-bold text-2xl mt-5">LocalFold Setup</header>
      <label className="text-center flex flex-col justify-center font-bold mt-10 mb-10">
        Select Model Type
        <select
          defaultValue="auto"
          className="bg-black text-center font-light"
          onChange={(option) => {
            setup.modelType = option.target.value
          }}
        >
          <option value="AlphaFold2-multimer-v1">AlphaFold2-multimer-v1</option>
          <option value="AlphaFold2-multimer-v2">AlphaFold2-multimer-v2</option>
          <option value="auto">Auto</option>
        </select>
      </label>
      <button
        className="text-white bg-transparent mt-2 hover:text-gray-200"
        onClick={modelParametersSetup}
      >
        Select Parameters
      </button>
      <button
        className="text-white bg-transparent mt-2 hover:text-gray-200"
        onClick={resultDirSetup}
      >
        Select Results Directory
      </button>
      <button
        className="font-bold"
        onClick={() => {
          signalsWebsocket.send(
            JSON.stringify({
              execute: 'set_model_options',
              arg: setup
            })
          )
          setToggleSetup(!toggleSetup)
          toast.info('Saving Setup')
        }}
      >
        Finish Setup
      </button>
    </div>
  )
}

export default Setup
