import CardBack from "./cardback";


export default class CardHeap extends CardBack
{
    private leftCardsNum: number = 0
    private txtLeftCardsNum: cc.Label = null

    constructor(leftCardsNum: number)
    {
        super()
        this.leftCardsNum = leftCardsNum
        let node: cc.Node = new cc.Node()
        node.color = cc.Color.BLACK
        node.setPosition(0, 0)
        this.addChild(node)
        this.txtLeftCardsNum = node.addComponent(cc.Label)
        this.txtLeftCardsNum.string = `${leftCardsNum}`
    }

    decreaseCardsNum(num: number)
    {
        this.leftCardsNum -= num
        this.txtLeftCardsNum.string = `${this.leftCardsNum}`
    }
}
