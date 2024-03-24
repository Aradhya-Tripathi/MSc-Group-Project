import { signalsWebsocket } from '../Api'
import { toast } from 'sonner'

const Setup = ({ toggleSetup, setToggleSetup }) => {
  const modelSetup = () => {
    window.electron.ipcRenderer.send('model-selector')
    window.electron.ipcRenderer.on('model-selector-results', (_, msg) => {
      if (msg.filePath === undefined) return

      signalsWebsocket.send(
        JSON.stringify({
          execute: 'set_model_path',
          arg: msg.filePath[0]
        })
      )
      toast.success('Model Parameters Selected!')
    })
  }

  return (
    <div className="h-screen w-screen absolute bg-black flex flex-col items-center">
      <header className="text-white font-bold text-2xl mt-5">LocalFold Setup</header>
      <label className="text-center flex flex-col justify-center font-bold">
        Select Model Type
        <select defaultValue="Auto" className="bg-black text-center font-light">
          <option value="AlphaFold2-multimer-v1">AlphaFold2-multimer-v1</option>
          <option value="AlphaFold2-multimer-v2">AlphaFold2-multimer-v2</option>
          <option value="Auto">Auto</option>
        </select>
      </label>
      <button className="text-white bg-transparent mt-2 hover:text-gray-200" onClick={modelSetup}>
        Select Parameters
      </button>
      <button
        className="font-bold"
        onClick={() => {
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
