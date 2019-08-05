

export default class WebSocketClient
{
    static instance: WebSocketClient = new WebSocketClient()
    static connectSuccessCallBack: any = null
    static connectFailCallBack: any = null
    static closeByServerCallBack: any = null
    private sock: WebSocket = null
    private msgHandlers: Map<number, Function> = null

    constructor() {
        this.msgHandlers = new Map<number, Function>()
    }

    connect(ws_addr: string)
    {
        this.sock = new WebSocket(ws_addr)
        this.sock.onopen = this.onConnectted.bind(this)
        this.sock.onclose = this.onCloseSocket.bind(this)
        this.sock.onerror = this.onSocketError.bind(this)
        this.sock.onmessage = this.onReceivedMsg.bind(this)
    }

    onConnectted(event: any)
    {
        console.debug("Connect to server successfully")
        if (WebSocketClient.connectSuccessCallBack != null)
        {
            WebSocketClient.connectSuccessCallBack()
        }
    }

    onCloseSocket(event: any)
    {
        console.debug("Disconnect from server")
        if (WebSocketClient.closeByServerCallBack != null)
        {
            WebSocketClient.closeByServerCallBack()
        }
    }

    onSocketError(event: any)
    {
        console.debug("Socket Error")
        if (WebSocketClient.connectFailCallBack != null)
        {
            WebSocketClient.connectFailCallBack()
        }
    }

    close()
    {
        this.sock.close()
    }

    onReceivedMsg(event: any)
    {
        let data = JSON.parse(event.data)
        let msgId: number = data["msgId"]
        if (this.msgHandlers.has(msgId))
        {
            let handler: Function = this.msgHandlers.get(msgId)
            handler(data)
        }
        else
        {
            console.error(`Received unregistered message(${msgId})`)
        }
    }

    sendMsg(msg: any)
    {
        this.sock.send(JSON.stringify(msg))   
    }

    register(msgId: number, handler: Function)
    {
        if (this.msgHandlers.has(msgId))
        {
            console.error(`${msgId} was registerd`)
            return
        }
        this.msgHandlers.set(msgId, handler)
    }

    deregister(msgId: number)
    {
        if (!this.msgHandlers.has(msgId))
        {
            console.error(`${msgId} is not registered`)
            return
        }
        this.msgHandlers.delete(msgId)
    }

    static getInstance()
    {
        return WebSocketClient.instance
    }
}