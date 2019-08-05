import AbandonCard from "./abandon_card"

export default class AbandonCardManager
{
    private cards: AbandonCard[] = []
    private node: cc.Node = null

    constructor(node: cc.Node)
    {
        this.node = node
    }

    abandonCards(cards: number[])
    {
        for (let val of cards)
        {
            let card: AbandonCard = new AbandonCard(val)
            this.node.addChild(card)
            this.cards.push(card)
        }
        this.arrangeCards()
    }

    clear()
    {
        let len: number = this.cards.length
        for (let i: number = 0; i < len; ++i)
        {
            this.cards[0].removeFromParent()
            this.cards.splice(0, 1)
        }
    }

    arrangeCards()
    {
        let cardsNum: number = this.cards.length
        if (cardsNum <= 0) { return }
        let cardWidth: number = 80
        let startX: number = 0 - ( cardWidth * cardsNum /2)
        for (let i: number = 0; i < cardsNum; ++i)
        {
            let x: number = startX + cardWidth * i
            this.cards[i].setPosition(x, 0)
        }
    }
}