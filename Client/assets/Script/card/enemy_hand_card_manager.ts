import CardBack from "./card_back";
import HandCardManager from "./hand_card_manager";


export default class EnemyHandCardManager extends HandCardManager
{
    cards: CardBack[] = []

    constructor(node: cc.Node)
    {
        super(node)
    }

    getSelectedHandCards(): number[]
    {
        return []
    }

    dispatchCards(cards: number[])
    {
        for (let _ of cards)
        {
            let handcard: CardBack = new CardBack()
            this.node.addChild(handcard)
            this.cards.push(handcard)
        }
        this.arrangeCards()
    }

    arrangeCards()
    {
        let cardsNum: number = this.cards.length
        if (cardsNum <= 0) { return }
        let uncorverWidthEachCard: number = 50
        let cardWidth: number = this.cards[cardsNum - 1].getContentSize().width
        let totalWidth: number = cardWidth + uncorverWidthEachCard * (cardsNum - 1)
        let startX: number = 0 - (totalWidth/2)
        for (let i: number = 0; i < cardsNum; ++i)
        {
            let x: number = startX + uncorverWidthEachCard * i
            this.cards[i].setPosition(x, 0)
            this.cards[i].zIndex = i
        }
    }

    deal(cards: number[])
    {
        for (let _ of cards)
        {
            this.cards[0].removeFromParent()
            this.cards.splice(0, 1)
        }
        this.arrangeCards()
    }
}