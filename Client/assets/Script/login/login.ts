const {ccclass, property} = cc._decorator;

import WebsocketClient from "../common/websocket_client"
import { OutMsgs } from "../messages/out_msgs"
import Player from "../player/player_info";

@ccclass
export default class Login extends cc.Component {
    private playerId: number = 0
    private wsServerAddr: string = ""
    private client: WebsocketClient = null

    start () {
        this.client = WebsocketClient.getInstance()
        this.node.getChildByName("ok").on(cc.Node.EventType.TOUCH_END, this.onClickOk, this)
        this.node.getChildByName("reset").on(cc.Node.EventType.TOUCH_END, this.onClickReset, this)
    }

    onClickOk()
    {
        let server_addr: string = this.node.getChildByName("server").getComponent("cc.EditBox").string
        let player_id: string = this.node.getChildByName("player").getComponent("cc.EditBox").string

        WebsocketClient.connectSuccessCallback = function() {
            let playerId: number =  Number(player_id)
            let msg = {"msgId": OutMsgs.PLAYER_LOGIN_IND, "playerId": playerId}
            WebsocketClient.sendMessage(msg)
            Player.playerId = playerId
            cc.director.loadScene("hall")
        }
        WebsocketClient.connectFailCallback = function() {
            this.node.getChildByName("notice").getComponent(cc.Label).string = "连接服务器失败"
        }.bind(this)
        this.client.connect(server_addr)
    }

    onClickReset()
    {
        this.node.getChildByName("server").getComponent("cc.EditBox").string = ""
        this.node.getChildByName("player").getComponent("cc.EditBox").string = ""
        this.node.getChildByName("notice").getComponent(cc.Label).string = ""
    }
}
