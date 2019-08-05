const {ccclass, property} = cc._decorator;

import TwoPlayersRoomModel from "./two_players_room_model"
import CardHeap from "../../card/card_heap"
import WebSocketClient from "../../socket/websocket_client";
import {InMsgs} from "../../msg/in_msgs"
import {OutMsgs} from "../../msg/out_msgs"
import UserInfo from "../../user/user_info";
import CardComparator from "../../card/card_comparator";

@ccclass
export default class TwoPlayersRoomCtrl extends cc.Component
{
    private model: TwoPlayersRoomModel = null
    private roomId: number = 0
    private cardHeap: CardHeap = null
    private wsClient: WebSocketClient = null

    start()
    {
        this.cardHeap = new CardHeap()
        this.node.addChild(this.cardHeap)
        this.cardHeap.setPosition(-340, 0)

        this.model = new TwoPlayersRoomModel(this.node.getChildByName("player1"), this.node.getChildByName("player2"))

        this.wsClient = WebSocketClient.getInstance()
        this.wsClient.register(InMsgs.DEAL_OWNER_CHANGE_IND, this.handleDealOwnerChange.bind(this))
        this.wsClient.register(InMsgs.DISPATCH_CARDS_IND, this.handleDispatchCards.bind(this))
        this.wsClient.register(InMsgs.GAME_START_IND, this.handleGameStart.bind(this))
        this.wsClient.register(InMsgs.GAME_OVER_IND, this.handleGameOver.bind(this))
        this.wsClient.register(InMsgs.PLAYER_DEAL_IND, this.handlePlayerDeal.bind(this))
        this.wsClient.register(InMsgs.PLAYER_PASS_IND, this.handlePlayerPass.bind(this))
        this.wsClient.register(InMsgs.PLAYER_JOIN_ROOM_IND, this.handlePlayerJoinRoom.bind(this))
        this.wsClient.register(InMsgs.PLAYER_LEAVE_ROOM_IND, this.handlePlayerLeaveRoom.bind(this))
        this.wsClient.register(InMsgs.PLAYER_GET_SCORE_IND, this.handlePlayerGetScore.bind(this))
        this.wsClient.register(InMsgs.PLAYER_READY_IND, this.handlePlayerReady.bind(this))
        this.wsClient.register(InMsgs.ROOM_INFO_IND, this.handleGetRoomInfo.bind(this))

        this.node.getChildByName("player1").getChildByName("ready").on(cc.Node.EventType.TOUCH_END, this.ready, this)
        this.node.getChildByName("player1").getChildByName("leave").on(cc.Node.EventType.TOUCH_END, this.leaveRoom, this)
        this.node.getChildByName("player1").getChildByName("pass").on(cc.Node.EventType.TOUCH_END, this.pass, this)
        this.node.getChildByName("player1").getChildByName("deal").on(cc.Node.EventType.TOUCH_END, this.deal, this)

        this.enterRoom()
    }

    handleGetRoomInfo(msg: any)
    {
        for (let playerInfo of msg["players"])
        {
            if (playerInfo["playerId"] == UserInfo.userId)
            {
                this.node.getChildByName("roominfo").getChildByName("player1").getComponent(cc.Label).string = `${UserInfo.userId}`
                this.roomId = playerInfo["roomId"]
                this.node.getChildByName("roominfo").getChildByName("roomid").getComponent(cc.Label).string = `房号: ${this.roomId}`
                this.model.player1SitDown(playerInfo["playerId"], playerInfo["index"])
            }
            else
            {
                this.node.getChildByName("roominfo").getChildByName("player2").getComponent(cc.Label).string = `${playerInfo["playerId"]}`
                this.model.player2SitDown(playerInfo["playerId"], playerInfo["index"])
                this.model.ready(playerInfo["playerId"], playerInfo["isReady"])
            }
        }

    }

    handlePlayerGetScore(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        this.model.changePlayerScore(msg["playerId"], msg["scoreInTotal"])
    }

    handlePlayerReady(msg: any)
    {
        var playerInfo = msg["playerInfo"]
        if (playerInfo["roomId"] != this.roomId) { return }
        this.model.ready(playerInfo["playerId"], playerInfo["isReady"])
    }

    handlePlayerJoinRoom(msg: any)
    {
        var playerInfo = msg["playerInfo"]
        if (playerInfo["roomId"] != this.roomId) { return }
        if (playerInfo["playerId"] == UserInfo.userId) { return }
        if (!this.model.isPlayer2Exist())
        {
            this.model.player2SitDown(playerInfo["playerId"], playerInfo["index"])
            this.node.getChildByName("roominfo").getChildByName("player2").getComponent(cc.Label).string = `${playerInfo["playerId"]}`
        }
    }

    handlePlayerLeaveRoom(msg: any)
    {
        var playerInfo = msg["playerInfo"]
        if (playerInfo["roomId"] != this.roomId) { return }
        if (playerInfo["playerId"] == UserInfo.userId) { return }
        if (this.model.isPlayer2Exist())
        {
            this.model.player2SitUp()
            this.node.getChildByName("roominfo").getChildByName("player2").getComponent(cc.Label).string = ""
        }
    }

    handleDispatchCards(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        let playerId: number = msg["playerId"]
        if (playerId != UserInfo.userId) { return }
        let p1Cards: number[] = msg["cards"]
        let p2Cards: number[] = []
        let cardsNumP2Want: number = 5 - this.model.getP2HandCardsNum()
        if (cardsNumP2Want > this.cardHeap.cardsNumLeft)
        {
            cardsNumP2Want = this.cardHeap.cardsNumLeft
        }
        for (let i: number = 0; i < cardsNumP2Want; ++i)
        {
            p2Cards.push(0)
        }
        this.model.dispatchCards(p1Cards, p2Cards)
        this.cardHeap.decreaseCards(p1Cards.length + p2Cards.length)
    }

    handleGameStart(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        this.node.getChildByName("player1").getChildByName("ready").active = false
        this.node.getChildByName("player1").getChildByName("leave").active = false
        this.node.getChildByName("player1").getChildByName("pass").active = true
        this.node.getChildByName("player1").getChildByName("deal").active = true
        this.model.gamestart()
    }

    handleGameOver(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        this.node.getChildByName("player1").getChildByName("ready").active = true
        this.node.getChildByName("player1").getChildByName("leave").active = true
        this.node.getChildByName("player1").getChildByName("pass").active = false
        this.node.getChildByName("player1").getChildByName("deal").active = false
        this.model.gameover()
    }

    handlePlayerDeal(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        if (msg["playerId"] == UserInfo.userId) { return }
        this.model.deal(msg["playerId"], msg["cards"])
    }

    handlePlayerPass(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        if (msg["playerId"] == UserInfo.userId) { return }
        this.model.pass(msg["playerId"])
    }

    handleDealOwnerChange(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        this.model.changeDealOwner(msg["playerId"])
    }

    enterRoom()
    {
        var playerEnterRoomInd = {"msgId": OutMsgs.PLAYER_ENTER_ROOM_IND, "playerId": UserInfo.userId, "roomType": 0}
        this.wsClient.sendMsg(playerEnterRoomInd)
        this.node.getChildByName("player1").getChildByName("ready").active = true
        this.node.getChildByName("player1").getChildByName("leave").active = true
        this.node.getChildByName("player1").getChildByName("pass").active = false
        this.node.getChildByName("player1").getChildByName("deal").active = false
    }

    leaveRoom()
    {
        this.wsClient.deregister(InMsgs.DEAL_OWNER_CHANGE_IND)
        this.wsClient.deregister(InMsgs.DISPATCH_CARDS_IND)
        this.wsClient.deregister(InMsgs.GAME_START_IND)
        this.wsClient.deregister(InMsgs.GAME_OVER_IND)
        this.wsClient.deregister(InMsgs.PLAYER_DEAL_IND)
        this.wsClient.deregister(InMsgs.PLAYER_PASS_IND)
        this.wsClient.deregister(InMsgs.PLAYER_JOIN_ROOM_IND)
        this.wsClient.deregister(InMsgs.PLAYER_LEAVE_ROOM_IND)
        this.wsClient.deregister(InMsgs.PLAYER_GET_SCORE_IND)
        this.wsClient.deregister(InMsgs.PLAYER_READY_IND)
        this.wsClient.deregister(InMsgs.ROOM_INFO_IND)
        
        let leaveRoomInd = {"msgId": OutMsgs.PLAYER_LEAVE_ROOM_IND, "playerId": UserInfo.userId, "roomId": this.roomId}
        this.wsClient.sendMsg(leaveRoomInd)

        cc.director.loadScene("hall")
    }

    ready()
    {
        var playerReadyInd = {"msgId": OutMsgs.PLAYER_READY_IND, "playerId": UserInfo.userId, "roomId": this.roomId, "isReady": true}
        this.wsClient.sendMsg(playerReadyInd)
    }

    pass()
    {
        var playerReadyInd = {"msgId": OutMsgs.PLAYER_PASS_IND, "playerId": UserInfo.userId, "roomId": this.roomId}
        this.wsClient.sendMsg(playerReadyInd)
    }

    deal()
    {
        let cards: number[] = this.model.getPlayer1SelectedCards()
        if (!CardComparator.isCardTypeLeagal(cards)) { return }
        if (CardComparator.compare(cards, this.model.p2LatestCards) < 0) { return }
        var playerPassInd = {"msgId": OutMsgs.PLAYER_DEAL_IND, "playerId": UserInfo.userId, "roomId": this.roomId, "cards": cards}
        this.wsClient.sendMsg(playerPassInd)
    }

    cleanTheRoom()
    {
    }
}