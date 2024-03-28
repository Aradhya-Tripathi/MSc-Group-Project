import { electronApp, is, optimizer } from '@electron-toolkit/utils'
import { app, BrowserWindow, dialog, ipcMain, shell } from 'electron'
import { join } from 'path'
import { exec } from 'child_process'

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    // ...(process.platform === 'linux' ? { icon } : {}), // Fix this icon issue for MacOS
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
  return mainWindow
}
ipcMain.on('ping', () => console.log('pong'))

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  const mainWindow = createWindow()
  // Custom Event Handlers

  mainWindow.on('close', (event) => {
    let response = dialog.showMessageBoxSync(mainWindow, {
      title: 'Confirm Closing',
      type: 'info',
      buttons: ['Leave', 'Stay'],
      defaultId: 1,
      message: 'Closing Confirmation',
      detail: 'Closing the application will remove all scheduled/exeuting jobs.',
      icon: '/Users/aradhya/Desktop/Uni-Projects/group-project/ui/resources/icon.png'
    })
    if (response === 1) event.preventDefault()
    else {
      mainWindow.webContents.send('closing')
      app.exit(0)
    }
  })

  // Custom Messages
  ipcMain.on('query-selector', () => {
    let filePath = dialog.showOpenDialogSync(mainWindow, {
      title: 'Select query file',
      message: 'Selected file will be used as input to the model',
      properties: ['openFile'],
      filters: [{ name: 'CSV Files', extensions: ['csv'] }]
    })
    mainWindow.webContents.send('query-selector-results', { filePath: filePath })
  })

  ipcMain.on('model-selector', () => {
    let filePath = dialog.showOpenDialogSync(mainWindow, {
      title: 'Select Model Parameters',
      message: 'Selected directory will be use to set parameters for model inference',
      properties: ['openDirectory']
    })
    mainWindow.webContents.send('model-selector-results', { filePath: filePath })
  })

  ipcMain.on('results-dir-selector', () => {
    let filePath = dialog.showOpenDialogSync(mainWindow, {
      title: 'Select Results Direcotry',
      message: 'Model predictions will be save in this directory',
      properties: ['openDirectory']
    })
    mainWindow.webContents.send('results-dir-results', { filePath: filePath })
  })

  ipcMain.on('clicked-prediction', (event, msg) => {
    exec(`pymol ${msg.resultDestination}/*.pdb`, (err, stdout, stderr) => {
      console.log(stdout)
    })
  })

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.dock.setIcon(join(__dirname, '../../resources/icon.png'))
