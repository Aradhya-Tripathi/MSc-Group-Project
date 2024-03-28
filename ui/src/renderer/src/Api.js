import axios from 'axios'

export const wsbaseURL = 'ws://localhost:8000'
export const baseURL = 'http://localhost:8000'

export const signalsWebsocket = new WebSocket(wsbaseURL + '/ws/signals')
export const dataApi = axios.create({
  baseURL: 'http://localhost:8000'
})
