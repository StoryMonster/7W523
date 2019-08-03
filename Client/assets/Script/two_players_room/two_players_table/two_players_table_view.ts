const {ccclass, property} = cc._decorator;

import TwoPlayersTableModel from "./two_players_table_model"
import { PlayerStatus } from "../../common/player_status"
import Card from "../../common/cards/card"
import CardHeap from "../../common/cards/cardheap";

@ccclass
export default class TwoPlayersTableView extends cc.Component {
    private btnReady: cc.Node = null
    private btnLeave: cc.Node = null
    private btnDeal:  cc.Node = null
    private btnPass:  cc.Node = null
    private cardHeap: CardHeap = null
    private model: TwoPlayersTableModel = null
    private roomInfo: cc.Node = null

    start () {
        this.initControlPanel()
        this.initCardHeap()
        this.initRoomInfo()
        this.model = new TwoPlayersTableModel(this)
    }

    initControlPanel()
    {
        let control: cc.Node = this.node.getChildByName("control")
        this.btnReady = control.getChildByName("ready")
        this.btnReady.active = true
        this.btnReady.on(cc.Node.EventType.TOUCH_END, this.ready, this)

        this.btnLeave = control.getChildByName("leave")
        this.btnLeave.active = true
        this.btnLeave.on(cc.Node.EventType.TOUCH_END, this.leave, this)

        this.btnDeal = control.getChildByName("deal")
        this.btnDeal.active = false
        this.btnDeal.on(cc.Node.EventType.TOUCH_END, this.deal, this)

        this.btnPass = control.getChildByName("pass")
        this.btnPass.active = false
        this.btnPass.on(cc.Node.EventType.TOUCH_END, this.pass, this)
    }

    initCardHeap()
    {
        this.cardHeap = new CardHeap(54)
        this.cardHeap.setPosition(-430, 0)
        this.node.addChild(this.cardHeap)
    }

    initRoomInfo()
    {
        this.roomInfo = this.node.getChildByName("roominfo")
    }

    updateRoomInfo(roomId: number)
    {
        this.roomInfo.getChildByName("roomid").getComponent(cc.Label).string = `RoomId: ${roomId}`
    }

    setPlayer1GeneralInfo(info: string)
    {
        this.roomInfo.getChildByName("player1").getComponent(cc.Label).string = info
    }

    setPlayer2GeneralInfo(info: string)
    {
        this.roomInfo.getChildByName("player2").getComponent(cc.Label).string = info
    }

    ready()
    {
        this.model.informServerReady()
    }

    leave()
    {
        this.model.leaveRoom()
        this.destroy()
        cc.director.loadScene("hall")
    }

    deal()
    {
        this.model.deal()
    }

    pass()
    {
        this.model.pass()
    }

    gameStart()
    {
        this.activeGameProcessControl(false, false)
    }

    gameOver()
    {
        this.activeDealControl(false, false)
        this.activeGameProcessControl(true, true)
    }

    activeDealControl(deal: boolean, pass: boolean)
    {
        this.btnDeal.active = deal
        this.btnPass.active = pass
    }

    activeGameProcessControl(ready: boolean, leave: boolean)
    {
        this.btnReady.active = ready
        this.btnLeave.active = leave
    }

    decreaseCardHeap(num: number)
    {
        this.cardHeap.decreaseCardsNum(num)
    }
}
