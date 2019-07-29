import { PlayerStatus } from "../../common/player_status"
import WebsocketClient from "../../common/websocket_client"
import TwoPlayersTableView from "./two_players_table_view"
import { OutMsgs } from "../../messages/out_msgs"
import { InMsgs} from "../../messages/in_msgs"
import PlayerCardsManager from "../../common/cards/player_cards_manager";
import EnemyCardsManager from "../../common/cards/enemy_cards_manager";

export default class TwoPlayersTableModel
{
    private player1Status: PlayerStatus = PlayerStatus.None
    private player2Status: PlayerStatus = PlayerStatus.None
    private p1CardsManager: PlayerCardsManager = null
    private p2CardsManager: EnemyCardsManager = null
    private player1DealedCards: number[] = []
    private player2DealedCards: number[] = []
    private client: WebsocketClient = null
    private view: TwoPlayersTableView = null

    constructor(view: TwoPlayersTableView)
    {
        this.view = view
        this.client = WebsocketClient.getInstance()
        this.client.register(InMsgs.CARDS_DISPATCH_IND, this.handleCardsDispatchInd.bind(this) )
        this.client.register(InMsgs.GAME_START_IND, this.handleGameStart.bind(this))
        this.client.register(InMsgs.GAME_OVER_IND, this.handleGameOver.bind(this))
        this.client.register(InMsgs.ROOM_INFO_IND, this.handGetRoomInfo.bind(this))
        this.client.sendMessage(OutMsgs.CLIENT_CHOOSE_ROOM_IND, {})

        this.p1CardsManager = new PlayerCardsManager(this.view.node.getChildByName("player1"))
        this.p2CardsManager = new EnemyCardsManager(this.view.node.getChildByName("player2"))
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
        this.view.updatePlayer1Status(status)
    }

    setPlayer2Status(status: PlayerStatus = PlayerStatus.None)
    {
        this.player2Status = status
        this.view.updatePlayer2Status(status)
    }

    tellServerPlayer1Ready()
    {
        this.client.sendMessage(OutMsgs.CLIENT_READY_IND, {})
    }

    tellServerPlayer1NotReady()
    {
        this.client.sendMessage(OutMsgs.CLIENT_NOT_READY_IND, {})
    }

    handleCardsDispatchInd(msg: any)
    {
        let cardIds: number[] = msg["cardIds"]
        this.p1CardsManager.dispatchCards(cardIds)
        this.p2CardsManager.dispatchCards()
    }

    handleGameStart(msg: any)
    {
        this.view.gameStart()
    }

    handleGameOver(msg: any)
    {
        this.view.gameOver()
    }

    handGetRoomInfo(msg: any)
    {
        let roomId: number = msg["roomId"]
        this.view.updateRoomInfo(roomId)
    }

    deal()
    {
        this.p1CardsManager.deal()
    }

    pass()
    {
        this.p1CardsManager.pass()
        // TODO: 向server发送回合结束消息
    }
}