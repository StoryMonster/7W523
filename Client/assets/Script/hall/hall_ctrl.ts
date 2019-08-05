const {ccclass, property} = cc._decorator;

@ccclass
export default class HallCtrl extends cc.Component
{
    start()
    {
        let btn2PRoom: cc.Node = this.node.getChildByName("btn_two_players_room")
        let btn3PRoom: cc.Node = this.node.getChildByName("btn_three_players_room")
        btn2PRoom.on(cc.Node.EventType.TOUCH_END, this.onTwoPlayersRoomClicked, this)
        btn3PRoom.on(cc.Node.EventType.TOUCH_END, this.onThreePlayersRoomClicked, this)
    }

    onTwoPlayersRoomClicked()
    {
        cc.director.loadScene("two_players_room")
    }

    onThreePlayersRoomClicked()
    {}
}
