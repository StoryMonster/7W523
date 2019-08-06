const {ccclass, property} = cc._decorator;

import TwoPlayersRoomModel from "./two_players_room_model"
import CardHeap from "../../card/card_heap"
import WebSocketClient from "../../socket/websocket_client";
import {InMsgs} from "../../msg/in_msgs"
import {OutMsgs} from "../../msg/out_msgs"
import UserInfo from "../../user/user_info";
import CardComparator from "../../card/card_comparator";
import { GameResult } from "../../common/game_result";

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
        this.cardHeap.decreaseCards(p1Cards.length)
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
        this.cardHeap.decreaseCards(p2Cards.length)
    }

    handleGameStart(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        this.node.getChildByName("player1").getChildByName("ready").active = false
        this.node.getChildByName("player1").getChildByName("leave").active = false
        this.node.getChildByName("player1").getChildByName("pass").active = true
        this.node.getChildByName("player1").getChildByName("deal").active = true
        this.cardHeap.cardsNumLeft = 54
        this.cardHeap.decreaseCards(0)
        this.model.gamestart()
    }

    handleGameOver(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        this.node.getChildByName("player1").getChildByName("ready").active = true
        this.node.getChildByName("player1").getChildByName("leave").active = true
        this.node.getChildByName("player1").getChildByName("pass").active = false
        this.node.getChildByName("player1").getChildByName("deal").active = false
        let p2HandCards: number[] = []
        for (let playerInfo of msg["res"])
        {
            if (playerInfo["playerId"] != UserInfo.userId)
            {
                p2HandCards = playerInfo["cards"]
                break
            }
        }
        this.model.gameover(p2HandCards)
        let node = new cc.Node()
        this.node.addChild(node)
        node.on(cc.Node.EventType.TOUCH_END, function(){ node.removeFromParent() })
        let sp: cc.Sprite = node.addComponent(cc.Sprite)
        switch(this.model.getGameResult())
        {
            case GameResult.Win: sp.spriteFrame = new cc.SpriteFrame(cc.url.raw("resources/result/win.jpg")); break;
            case GameResult.Fail: sp.spriteFrame = new cc.SpriteFrame(cc.url.raw("resources/result/fail.jpg")); break
            case GameResult.Draw: sp.spriteFrame = new cc.SpriteFrame(cc.url.raw("resources/result/draw.jpg")); break;
        }
    }

    handlePlayerDeal(msg: any)
    {
        if (msg["roomId"] != this.roomId) { return }
        //if (msg["playerId"] == UserInfo.userId) { return }
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
        // 牌型合法性判断
        if (!CardComparator.isCardTypeLeagal(cards)) { return }
        // 扯判断
        let lastP1Cards: number[] = this.model.getP1LastThrownCards()
        let lastP2Cards: number[] = this.model.getP2LastThrownCards()
        let lvlLastP1Cards: number = CardComparator.getCardsLevel(lastP1Cards)
        let lvlLastP2Cards: number = CardComparator.getCardsLevel(lastP2Cards)
        let lvl: number = CardComparator.getCardsLevel(cards)
        if (lvlLastP1Cards == 1 && lvlLastP2Cards == 2 && lastP1Cards[0] % 13 == lastP2Cards[0] % 13)
        {
            if (lvl != 5 && lvl != 4) { return }
        }
        else if (lvlLastP2Cards == 1 && lvl == 2 && cards[0] % 13 != lastP2Cards[0] % 13) { return }
        else if (CardComparator.compare(cards, lastP2Cards) < 0) { return }
        var playerPassInd = {"msgId": OutMsgs.PLAYER_DEAL_IND, "playerId": UserInfo.userId, "roomId": this.roomId, "cards": cards}
        this.wsClient.sendMsg(playerPassInd)
    }
}