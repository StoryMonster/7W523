import HandCardManager from "./hand_card_manager";
import HandCard from "./hand_card";


export default class PlayerHandCardManager extends HandCardManager
{
    cards: HandCard[] = []

    constructor(node: cc.Node)
    {
        super(node)
    }

    dispatchCards(cards: number[])
    {
        for (let card of cards)
        {
            let handcard: HandCard = new HandCard(card)
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
        let cardWidth: number = this.cards[0].getContentSize().width
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
        for (let i: number = this.cards.length - 1; i >= 0; --i)
        {
            for (let val of cards)
            {
                if (this.cards[i].value == val)
                {
                    this.cards[i].removeFromParent()
                    this.cards.splice(i, 1)
                    break
                }
            }
        }
        this.arrangeCards()
    }

    getSelectedHandCards(): number[]
    {
        let cards: number[] = []
        for (let card of this.cards)
        {
            if (card.isSelected)
            {
                cards.push(card.value)
            }
        }
        return cards
    }
}