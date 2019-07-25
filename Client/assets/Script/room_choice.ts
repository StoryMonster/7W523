const {ccclass, property} = cc._decorator;

@ccclass
export default class RoomChoicePage extends cc.Component {
    private btn2PlayersRoom: cc.Node = null
    private btn3PlayersRoom: cc.Node = null

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
    }

    onChoose2PlayersRoom()
    {
        cc.director.loadScene("two_players_room")
    }

    onChoose3PlayersRoom()
    {
    }
}
