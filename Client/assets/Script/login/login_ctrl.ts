const {ccclass, property} = cc._decorator;

import WebSockectClient from "../socket/websocket_client"
import UserInfo from "../user/user_info"
import {OutMsgs} from "../msg/out_msgs"
import WebSocketClient from "../socket/websocket_client";

@ccclass
export default class LoginCtrl extends cc.Component
{
    start()
    {
        this.node.getChildByName("ok").on(cc.Node.EventType.TOUCH_END, this.onOkClicked, this)
        this.node.getChildByName("reset").on(cc.Node.EventType.TOUCH_END, this.onResetClicked, this)
    }

    onOkClicked()
    {
        let serverAddr: string = this.node.getChildByName("server").getComponent("cc.EditBox").string
        // TODO: serverAddr 格式检查
        let userId: number = Number(this.node.getChildByName("player").getComponent("cc.EditBox").string)
        // TODO: userId 格式检查
        WebSockectClient.connectSuccessCallBack = function() {
            UserInfo.userId = userId
            let msg = {"msgId": OutMsgs.PLAYER_LOGIN_IND, "playerId": userId}
            WebSocketClient.getInstance().sendMsg(msg)
            cc.director.loadScene("hall")
        }
        WebSocketClient.connectFailCallBack = function() {
            this.node.getChildByName("notice").getComponent(cc.Label).string = "连接服务器失败"
        }.bind(this)
        WebSocketClient.getInstance().connect(serverAddr)
    }

    onResetClicked()
    {
        this.node.getChildByName("server").getComponent("cc.EditBox").string = ""
        this.node.getChildByName("player").getComponent("cc.EditBox").string = ""
        this.node.getChildByName("notice").getComponent(cc.Label).string = ""
    }
}