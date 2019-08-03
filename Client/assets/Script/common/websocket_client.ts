import MsgHandlerManager from "./message_handler_manager"
import { InMsgs} from "../messages/in_msgs"

export default class WebsocketClient
{
    private static sock: WebSocket = null
    private msgHandlerManager: MsgHandlerManager = null
    public static connectSuccessCallback: any = null
    public static connectFailCallback: any = null
    public static instance: WebsocketClient = new WebsocketClient()

    private constructor()
    {
        this.msgHandlerManager = new MsgHandlerManager()
    }

    public connect(addr: string)
    {
        WebsocketClient.sock = new WebSocket(addr)
        WebsocketClient.sock.onopen = this.onConnectServer
        WebsocketClient.sock.onclose = this.onCloseConnection
        WebsocketClient.sock.onmessage = this.onReceivedMessage
        WebsocketClient.sock.onerror = this.onWebSocketError
    }

    public static getInstance(): WebsocketClient
    {
        return WebsocketClient.instance
    }

    onConnectServer(event: Event): any
    {
        console.log("Connectted to server successfully")
        if (WebsocketClient.connectSuccessCallback != null)
        {
            WebsocketClient.connectSuccessCallback()
        }
    }

    onWebSocketError(event: Event): any
    {
        console.log("Something error on the websocket connection")
        if (WebsocketClient.connectFailCallback != null)
        {
            WebsocketClient.connectFailCallback()
        }
    }

    onReceivedMessage(event: any): any
    {
        let decoded = JSON.parse(event.data)
        let handler = WebsocketClient.instance.msgHandlerManager.getHandler(decoded["msgId"])
        if (handler == null)
        {
            console.error(`No handler found for ${decoded["msgId"]}`)
            return
        }
        handler(decoded)
    }

    onCloseConnection(event: Event): any
    {
        console.log("disconnect from server")
    }

    static sendMessage(msg: any)
    {
        WebsocketClient.sock.send(JSON.stringify(msg))
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
