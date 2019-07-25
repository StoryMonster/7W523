const {ccclass, property} = cc._decorator;

import TwoPlayersTableModel from "./two_players_table_model"
import { PlayerStatus } from "../../common/player_status"

@ccclass
export default class TwoPlayersTableView extends cc.Component {
    private btnReady: cc.Node = null
    private btnLeave: cc.Node = null
    private btnDeal:  cc.Node = null
    private btnPass:  cc.Node = null
    private cardHeap: cc.Node = null
    private txtCardHeapHeight: cc.Node = null
    private player1HandCards: cc.Node = null
    private player1PlayedCards: cc.Node = null
    private player1Status: cc.Node = null
    private player1Score: cc.Node = null
    private player2HandCards: cc.Node = null
    private player2PlayedCards: cc.Node = null
    private player2Status: cc.Node = null
    private player2Score: cc.Node = null
    private model: TwoPlayersTableModel = null

    start () {
        this.initControlPanel()
        this.initPlayer1Area()
        this.initPlayer2Area()
        this.initCardHeap()
        this.model = new TwoPlayersTableModel()
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

    initPlayer1Area()
    {
        let player1Area: cc.Node = this.node.getChildByName("player1")
        this.player1HandCards = player1Area.getChildByName("handcards")
        this.player1PlayedCards = player1Area.getChildByName("playedcards")
        this.player1Status = player1Area.getChildByName("status")
        this.player1Score = player1Area.getChildByName("score")
        if (this.player1Score) { this.player1Score.getComponent(cc.Label).string = "" }
        if (this.player1Status) { this.player1Status.getComponent(cc.Label).string = "" }
    }

    initPlayer2Area()
    {
        let player2Area: cc.Node = this.node.getChildByName("player2")
        this.player2HandCards = player2Area.getChildByName("handcards")
        this.player2PlayedCards = player2Area.getChildByName("playedcards")
        this.player2Status = player2Area.getChildByName("status")
        this.player2Score = player2Area.getChildByName("score")

        if (this.player2Score) { this.player2Score.getComponent(cc.Label).string = "" }
        if (this.player2Status) { this.player2Status.getComponent(cc.Label).string = "" }
    }

    initCardHeap()
    {
        this.cardHeap = this.node.getChildByName("cardheap")
        this.txtCardHeapHeight = this.cardHeap.getChildByName("cards_left")
        if (this.txtCardHeapHeight)
        {
            this.txtCardHeapHeight.getComponent(cc.Label).string = ""
        }
    }

    ready()
    {
        if (this.player1Status)
        {
            let label = this.player1Status.getComponent(cc.Label)
            if (this.model.getPlayer1Status() == PlayerStatus.None)
            {
                this.model.setPlayer1Status(PlayerStatus.Ready)
                label.string = "准备"
                this.model.tellServerPlayer1Ready()
            }
            else {
                this.model.setPlayer1Status(PlayerStatus.None)
                label.string = ""
                this.model.tellServerPlayer1NotReady()
            }
        }
    }

    leave()
    {
        this.destroy()
        cc.director.loadScene("room_choice")
    }

    deal()
    {}

    pass()
    {}
}
