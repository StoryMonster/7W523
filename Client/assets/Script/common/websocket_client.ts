import MsgHandlerManager from "./message_handler_manager"
import { OutMsgs } from "../messages/out_msgs"
import { InMsgs} from "../messages/in_msgs"

export default class WebsocketClient
{
    private sock: WebSocket = null
    private msgHandlerManager: MsgHandlerManager = null
    public static instance: WebsocketClient = new WebsocketClient()

    private constructor()
    {
        this.sock = new WebSocket("ws://127.0.0.1:12345")
        this.sock.onopen = this.onConnectServer
        this.sock.onclose = this.onCloseConnection
        this.sock.onmessage = this.onReceivedMessage
        this.sock.onerror = this.onCloseConnection

        this.msgHandlerManager = new MsgHandlerManager()
    }

    public static getInstance(): WebsocketClient
    {
         return WebsocketClient.instance
    }

    onConnectServer(event: Event): any
    {
        console.log("Connectted to server successfully")
    }

    onWebSocketError(event: Event): any
    {
        console.log("Something error on the websocket connection")
    }

    onReceivedMessage(event: any): any
    {
        let decoded = JSON.parse(event.data)
        let header = decoded["header"]
        let body = decoded["body"]
        let handler = WebsocketClient.instance.msgHandlerManager.getHandler(header["msgId"])
        if (handler == null)
        {
            console.error(`No handler found for ${header["msgId"]}`)
            return
        }
        handler(body)
    }

    onCloseConnection(event: Event): any
    {
        console.log("disconnect from server")
    }

    sendMessage(id: OutMsgs, msg: any)
    {
        let header = {"msgId": id, "playerId": 123}
        let data = {"header": header, "body": msg}
        this.sock.send(JSON.stringify(data))
    }

    register(msgId: number, handler: Function)
    {
        WebsocketClient.instance.msgHandlerManager.register(msgId, handler)
    }

    deregister(msgId: number)
    {
        WebsocketClient.instance.msgHandlerManager.deregister(msgId)
    }
}

