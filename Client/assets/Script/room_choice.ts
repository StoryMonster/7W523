const {ccclass, property} = cc._decorator;

import WebsocketClient from "./common/websocket_client"
import { OutMsgs } from "./messages/out_msgs"

@ccclass
export default class RoomChoicePage extends cc.Component {
    private btn2PlayersRoom: cc.Node = null
    private btn3PlayersRoom: cc.Node = null
    private websockClient: WebsocketClient = null

    start () {
        this.btn2PlayersRoom = this.node.getChildByName("btn_two_players_room")
        this.btn3PlayersRoom = this.node.getChildByName("btn_three_players_room")

        if (this.btn2PlayersRoom != null)
        {
            this.btn2PlayersRoom.on(cc.Node.EventType.TOUCH_END, this.onChoose2PlayersRoom, this)
        }

        if (this.btn3PlayersRoom != null)
        {
            this.btn3PlayersRoom.on(cc.Node.EventType.TOUCH_END, this.onChoose3PlayersRoom, this)
        }

        this.websockClient = WebsocketClient.getInstance()
        this.websockClient.sendMessage(OutMsgs.CLIENT_LOGIN_IND, {})
    }

    onChoose2PlayersRoom()
    {
        cc.director.loadScene("two_players_room")
    }

    onChoose3PlayersRoom()
    {
    }
}
