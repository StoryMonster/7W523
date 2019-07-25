import { PlayerStatus } from "../../common/player_status"

export default class TwoPlayersTableModel
{
    private player1Status: PlayerStatus = PlayerStatus.None
    private player2Status: PlayerStatus = PlayerStatus.None
    private sock: WebSocket = null

    constructor()
    {
        this.sock = new WebSocket("ws://127.0.0.1:12345")
        this.sock.onopen = this.onConnectServer
        this.sock.onclose = this.onCloseConnection
        this.sock.onmessage = this.onReceivedMessage
        this.sock.onerror = this.onCloseConnection
    }

    onConnectServer(event: Event): any
    {
        console.log("Connectted to server successfully")
    }

    onWebSocketError(event: Event): any
    {
        console.log("Something error on the websocket connection")
    }

    onReceivedMessage(event: Event): any
    {
        console.log("received message from server")
    }

    onCloseConnection(event: Event): any
    {
        console.log("disconnect from server")
    }

    getPlayer1Status(): PlayerStatus
    {
        return this.player1Status
    }

    getPlayer2Status(): PlayerStatus
    {
        return this.player2Status
    }

    setPlayer1Status(status: PlayerStatus = PlayerStatus.None)
    {
        this.player1Status = status
    }

    setPlayer2Status(status: PlayerStatus = PlayerStatus.None)
    {
        this.player2Status = status
    }

    tellServerPlayer1Ready()
    {
        let msg = {"playerId": 12}
        this.sock.send(JSON.stringify(msg))
    }

    tellServerPlayer1NotReady()
    {
    }
}