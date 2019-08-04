import Card from "./card";


export default class CardHeap extends Card
{
    private leftCardsNum: number = 0
    private txtLeftCardsNum: cc.Label = null

    constructor(leftCardsNum: number)
    {
        super(0)
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
        if (this.leftCardsNum < 0) { this.leftCardsNum = 0 }
        this.txtLeftCardsNum.string = `${this.leftCardsNum}`
    }

    getLeftCardsNum(): number
    {
        return this.leftCardsNum
    }
}
