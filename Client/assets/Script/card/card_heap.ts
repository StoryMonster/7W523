import CardBack from "./card_back";


export default class CardHeap extends CardBack
{
    cardsNumLeft: number = 54
    private lblCardsNumLeft: cc.Label = null

    constructor()
    {
        super()
        let node: cc.Node = new cc.Node()
        node.color = cc.Color.BLACK
        node.setPosition(0, 0)
        this.addChild(node)
        this.lblCardsNumLeft = node.addComponent(cc.Label)
        this.lblCardsNumLeft.string = `${this.cardsNumLeft}`
    }

    decreaseCards(num: number)
    {
        this.cardsNumLeft = this.cardsNumLeft - num
        if (this.cardsNumLeft < 0)
        {
            this.cardsNumLeft = 0
        }
        this.lblCardsNumLeft.string = `${this.cardsNumLeft}`
    }

}