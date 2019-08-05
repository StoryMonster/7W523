import Card from "./card";


export default class HandCardManager
{
    protected node: cc.Node = null

    constructor(node: cc.Node)
    {
        this.node = node
    }

    dispatchCards(cards: number[])
    {}

    deal(cards: number[])
    {}

    getHandCardsNum(): number { return 0 }

    arrangeCards()
    {}

    getSelectedHandCards(): number[] { return [] }
}