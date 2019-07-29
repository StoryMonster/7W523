

export default class MsgHandlerManager
{
    private handlers: Map<number, Function> = null
    constructor() {
        this.handlers = new Map<number, Function>()
    }

    register(msgId: number, handler: Function)
    {
        if (!this.handlers.has(msgId))
        {
            this.handlers.set(msgId, handler)
        }
        else
        {
            console.warn(`message ${msgId} was registered`)
        }
    }

    deregister(msgId: number)
    {
        if (!this.handlers.has(msgId))
        {
            console.warn(`message ${msgId} is never registerd ever`)
            return
        }
        this.handlers.delete(msgId)
    }

    getHandler(msgId: number): Function
    {
        if (this.handlers.has(msgId))
        {
            return this.handlers.get(msgId)
        }
        return null
    }

}