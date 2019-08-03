import { PlayerStatus } from "../../common/player_status"
import WebsocketClient from "../../common/websocket_client"
import TwoPlayersTableView from "./two_players_table_view"
import { OutMsgs } from "../../messages/out_msgs"
import { InMsgs} from "../../messages/in_msgs"
import PlayerCardsManager from "../../common/cards/player_cards_manager";
import EnemyCardsManager from "../../common/cards/enemy_cards_manager";
import Player from "../../player/player_info";
import PlayerInfoInRoom from "../../player/player_info_in_room";
import MsgHandlerManager from "../../common/message_handler_manager";

function getCardsLevel(cards: number[]): any
{
    let len: number = cards.length
    if (len == 1) { return 1 }
    if (len == 2 && ((cards[0] == 53 && cards[1] == 54) || (cards[0] == 54 && cards[1] == 53))) { return 5 }
    for (let i: number = 1; i < cards.length; ++i)
    {
        if (cards[0] % 13 != cards[i] % 13) { return 0 }
    }
    if (len == 2) { return 2}
    if (len == 3) { return 3}
    if (len == 4) { return 4}
    return 0
}

export default class TwoPlayersTableModel
{
    private player1: PlayerInfoInRoom = null
    private player2: PlayerInfoInRoom = null
    private p1GeneralInfo: string = ""
    private p2GeneralInfo: string = ""
    private client: WebsocketClient = null
    private view: TwoPlayersTableView = null
    private roomId: number = 0
    private latestUsedCards: number[] = []

    constructor(view: TwoPlayersTableView)
    {
        this.view = view
        let player1Node: cc.Node = this.view.node.getChildByName("player1")
        let player2Node: cc.Node = this.view.node.getChildByName("player2")
        this.player1 = new PlayerInfoInRoom(new PlayerCardsManager(player1Node), player1Node)
        this.player2 = new PlayerInfoInRoom(new EnemyCardsManager(player2Node), player2Node)

        this.client = WebsocketClient.getInstance()
        this.client.register(InMsgs.DISPATCH_CARDS_IND, this.handleCardsDispatchInd.bind(this) )
        this.client.register(InMsgs.GAME_START_IND, this.handleGameStart.bind(this))
        this.client.register(InMsgs.GAME_OVER_IND, this.handleGameOver.bind(this))
        this.client.register(InMsgs.ROOM_INFO_IND, this.handleRoomInfo.bind(this))
        this.client.register(InMsgs.PLAYER_DEAL_IND, this.handlePlayerDeal.bind(this))
        this.client.register(InMsgs.PLAYER_READY_IND, this.handlePlayerReady.bind(this))
        this.client.register(InMsgs.PLAYER_PASS_IND, this.handlePlayerPass.bind(this))
        this.client.register(InMsgs.DEAL_OWNER_CHANGE_IND, this.handleDealOwnerChange.bind(this))
        this.client.register(InMsgs.PLAYER_GET_SCORE_IND, this.hanlePlayerGetScore.bind(this))
        this.client.register(InMsgs.PLAYER_JOIN_ROOM_IND, this.handlePlayerJoinRoom.bind(this))
        this.client.register(InMsgs.PLAYER_LEAVE_ROOM_IND, this.handlePlayerLeaveRoom.bind(this))

        this.enterRoom()
    }

    private enterRoom()
    {
        var playerEnterRoomInd = {"msgId": OutMsgs.PLAYER_ENTER_ROOM_IND, "playerId": Player.playerId, "roomType": 0}
        WebsocketClient.sendMessage(playerEnterRoomInd)
    }

    leaveRoom()
    {
        this.client.deregister(InMsgs.DISPATCH_CARDS_IND)
        this.client.deregister(InMsgs.GAME_START_IND)
        this.client.deregister(InMsgs.GAME_OVER_IND)
        this.client.deregister(InMsgs.ROOM_INFO_IND)
        this.client.deregister(InMsgs.PLAYER_DEAL_IND)
        this.client.deregister(InMsgs.PLAYER_READY_IND)
        this.client.deregister(InMsgs.PLAYER_PASS_IND)
        this.client.deregister(InMsgs.DEAL_OWNER_CHANGE_IND)
        this.client.deregister(InMsgs.PLAYER_GET_SCORE_IND)
        this.client.deregister(InMsgs.PLAYER_JOIN_ROOM_IND)
        this.client.deregister(InMsgs.PLAYER_LEAVE_ROOM_IND)

        var playerLeaveRoomInd = {"msgId": OutMsgs.PLAYER_LEAVE_ROOM_IND, "playerId": this.player1.playerId, "roomId": this.roomId}
        WebsocketClient.sendMessage(playerLeaveRoomInd)

    }

    handleRoomInfo(msg: any)
    {   
        for (let playerInfo of msg["players"])
        {
            if (playerInfo["playerId"] == Player.playerId)
            {
                this.roomId = playerInfo["roomId"]
                this.view.updateRoomInfo(this.roomId)
                this.player1.index = playerInfo["index"]
                this.player1.playerId = playerInfo["playerId"]
                this.player1.setReady(playerInfo["isReady"])
                this.p1GeneralInfo = `${playerInfo["playerId"]}`
                this.view.setPlayer1GeneralInfo(this.p1GeneralInfo)
            }
            else
            {
                this.player2.index = playerInfo["index"]
                this.player2.playerId = playerInfo["playerId"]
                this.player2.setReady(playerInfo["isReady"])
                this.p2GeneralInfo = `${playerInfo["playerId"]}`
                this.view.setPlayer2GeneralInfo(this.p2GeneralInfo)
            }
        }
    }

    handlePlayerReady(msg: any)
    {
        var playerInfo = msg["playerInfo"]
        let roomId: number = playerInfo["roomId"]
        if (roomId != this.roomId)
        {
            return
        }
        let playerId: number = playerInfo["playerId"]
        if (playerId == this.player1.playerId)
        {
            this.player1.setReady(playerInfo["isReady"])
        }
        else if (playerId == this.player2.playerId)
        {
            this.player2.setReady(playerInfo["isReady"])
        }
    }

    handleCardsDispatchInd(msg: any)
    {
        let roomId: number = msg["roomId"]
        if (roomId != this.roomId) { return }
        let playerId: number = msg["playerId"]
        let cards: number[] = msg["cards"]
        if (playerId == this.player1.playerId)
        {
            this.view.decreaseCardHeap(5 - this.player1.getHandCardsNum())
            this.view.decreaseCardHeap(5 - this.player2.getHandCardsNum())
            this.player1.dispatchCards(cards)
            this.player2.dispatchCards([])
        }
        this.player1.setPass(false)
        this.player2.setPass(false)
        this.latestUsedCards = []
    }

    handleGameStart(msg: any)
    {
        let roomId: number = msg["roomId"]
        if (roomId != this.roomId) { return }
        this.player1.setReady(false)
        this.player2.setReady(false)
        this.player1.setScore(0)
        this.player2.setScore(0)
        this.view.gameStart()
    }

    handleGameOver(msg: any)
    {
        this.view.gameOver()
    }

    handlePlayerDeal(msg: any)
    {
        let roomId: number = msg["roomId"]
        if (roomId != this.roomId) { return }
        if (msg["playerId"] == this.player2.playerId)
        {
            this.player2.deal(msg["cards"])
        }
        this.latestUsedCards = msg["cards"]
    }

    handlePlayerPass(msg: any)
    {
        let roomId: number = msg["roomId"]
        if (roomId != this.roomId) { return }
        if (this.player2.playerId == msg["playerId"])
        {
            this.player2.setPass(true)
        }
    }

    handleDealOwnerChange(msg: any)
    {
        let roomId: number = msg["roomId"]
        if (roomId != this.roomId) { return }
        if (this.player1.playerId == msg["playerId"])
        {
            this.view.activeDealControl(true, true)
        }
        else
        {
            this.view.activeDealControl(false, false)
        }
    }

    hanlePlayerGetScore(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        if (msg["playerId"] == this.player1.playerId)
        {
            this.player1.setScore(msg["scoreInTotal"])
            this.player2.setScore(this.player2.score)
        }
        else if (msg["playerId"] == this.player2.playerId)
        {
            this.player1.setScore(this.player1.score)
            this.player2.setScore(msg["scoreInTotal"])
        }
    }

    handlePlayerJoinRoom(msg: any)
    {
        //if (this.p2GeneralInfo != "") { return }
        var playerInfo = msg["playerInfo"]
        if (playerInfo["roomId"] != this.roomId) { return }
        if (playerInfo["playerId"] == this.player1.playerId) { return }
        this.player2.index = playerInfo["index"]
        this.player2.playerId = playerInfo["playerId"]
        this.player2.sitdown()
        this.view.setPlayer2GeneralInfo(this.player2.generalInfo)
    }

    handlePlayerLeaveRoom(msg: any)
    {
        if (this.p2GeneralInfo == "") { return }
        var playerInfo = msg["playerInfo"]
        if (playerInfo["roomId"] != this.roomId) { return }
        if (playerInfo["playerId"] == this.player1.playerId) { return }
        this.player2.situp()
        this.view.setPlayer2GeneralInfo(this.player2.generalInfo)
    }

    informServerReady()
    {
        var playerReadyInd = {"msgId": OutMsgs.PLAYER_READY_IND, "playerId": this.player1.playerId, "roomId": this.roomId, "isReady": this.player1.isReady}
        WebsocketClient.sendMessage(playerReadyInd)
    }

    isBiggerThanLatestUsedCards(cards: number[]): any
    {
        let cardsLvl: number = getCardsLevel(cards)
        if (cardsLvl == 0) { return false }
        let refLvl: number = getCardsLevel(this.latestUsedCards)
        if (refLvl == 0) { return true }
        // 单牌判断
        if (refLvl == 1 && cardsLvl == 1)
        {
            let singleRankTable: number[] = [7, 54, 53, 5, 2, 3, 1, 0, 12, 11, 10, 9, 8, 6, 4]
            let val1: number = 0
            let val2: number = 0
            if (cards[0] == 54 || cards[0] == 53) { val1 = cards[0] }
            else { val1 = cards[0] % 13 }
            if (this.latestUsedCards[0] == 54 || this.latestUsedCards[0] == 53) { val2 = this.latestUsedCards[0] }
            else { val2 = this.latestUsedCards[0] % 13 }
            if (val1 == val2) { return true }
            for (let val of singleRankTable)
            {
                if (val == val1) { return true }
                if (val == val2) { return false }
            }
        }
        // 扯判断
        if (cardsLvl == 2 && refLvl ==1)
        {
            return cards[0] % 13 == this.latestUsedCards[0] % 13
        }
        // 王炸判断
        if (refLvl == 4 && cardsLvl == 5)
        {
            return this.latestUsedCards[0] % 13 != 7
        }
        if (refLvl == 5 && cardsLvl == 4)
        {
            return cards[0] % 13 == 7
        }
        // 同等牌数判断
        if (refLvl == cardsLvl)
        {
            if (cards[0]%13 == this.latestUsedCards[0]%13) { return true }
            let otherRankTable: number[] = [7, 5, 2, 3, 1, 0, 12, 11, 10, 9, 8, 6, 4]
            for (let val of otherRankTable)
            {
                if (val == cards[0]%13) { return true }
                if (val == this.latestUsedCards[0]%13) { return false } 
            }
        }
        return cardsLvl > refLvl
    }

    deal()
    {
        let cards: number[] = this.player1.getSelectedCards()
        if (!this.isBiggerThanLatestUsedCards(cards)) { return }
        var playerPassInd = {"msgId": OutMsgs.PLAYER_DEAL_IND, "playerId": this.player1.playerId, "roomId": this.roomId, "cards": cards}
        WebsocketClient.sendMessage(playerPassInd)
        this.player1.deal(cards)
        this.latestUsedCards = cards
    }

    pass()
    {
        var playerPassInd = {"msgId": OutMsgs.PLAYER_PASS_IND, "playerId": this.player1.playerId, "roomId": this.roomId}
        WebsocketClient.sendMessage(playerPassInd)
        this.player1.setPass(true)
    }
}
