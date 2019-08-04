import UsedCard from "./usedcard";
import HandCard from "./handcard";

export default class PlayerCardsManager implements CardsManager
{
    private usedCards: UsedCard[] = []
    private handCards: HandCard[] = []
    private handCardsNode: cc.Node = null
    private usedCardsNode: cc.Node = null

    constructor(node: cc.Node)
    {
        this.handCardsNode = node.getChildByName("handcards")
        this.usedCardsNode = node.getChildByName("playedcards")
    }

    dispatchCards(cards: number[])
    {
        this.clearUsedCards()
        for (let card of cards)
        {
            let handcard: HandCard = new HandCard(card)
            this.handCardsNode.addChild(handcard)
            this.handCards.push(handcard)
        }
        this.arrageHandCards()
    }

    setHandCards(cards: number[])
    {
        this.handCardsNode.removeAllChildren()
        for (let card of cards)
        {
            this.handCards.push(new HandCard(card))
        }
        this.arrageHandCards()
    }

    deal(_: number[])
    {
        let cards: number[] = this.getSelectHandCards()
        this.deleteSelectedHandCards()
        for (let card of cards)
        {
            this.addUsedCard(card)
        }
        this.arrangeUsedCards()
        this.arrageHandCards()
    }

    pass()
    {}

    getHandCardsNum(): number
    {
        return this.handCards.length
    }

    getSelectHandCards(): number[]
    {
        let cards: number[] = []
        for (let handcard of this.handCards)
        {
            if (handcard.isSelected())
            {
                cards.push(handcard.getValue())
            }
        }
        return cards
    }

    private deleteSelectedHandCards()
    {
        let len: number = this.handCards.length
        for (let i: number = len - 1; i >= 0; --i)
        {
            if (this.handCards[i].isSelected())
            {
                this.handCards[i].removeFromParent()
                this.handCards.splice(i, 1)
            }
        }
    }

    private addUsedCard(value: number)
    {
        let card: UsedCard = new UsedCard(value)
        this.usedCardsNode.addChild(card)
        this.usedCards.push(card)
    }

    private clearUsedCards()
    {
        let cardsNum: number = this.usedCards.length
        if (cardsNum <= 0) { return }
        for (let i: number = 0; i < cardsNum; ++i)
        {
            this.usedCards[i].removeFromParent()
        }
        this.usedCards = []
    }

    private arrangeUsedCards()
    {
        let cardsNum: number = this.usedCards.length
        if (cardsNum <= 0) { return }
        let cardWidth: number = 80
        let startX: number = 0 - ( cardWidth * cardsNum /2)
        for (let i: number = 0; i < cardsNum; ++i)
        {
            let x: number = startX + cardWidth * i
            this.usedCards[i].setPosition(x, 0)
        }
    }

    private arrageHandCards()
    {
        let cardsNum: number = this.handCards.length
        if (cardsNum <= 0) { return }
        let uncorverWidthEachCard: number = 50
        let cardWidth: number = this.handCards[cardsNum - 1].getContentSize().width
        let totalWidth: number = cardWidth + uncorverWidthEachCard * (cardsNum - 1)
        let startX: number = 0 - (totalWidth/2)
        for (let i: number = 0; i < cardsNum; ++i)
        {
            let x: number = startX + uncorverWidthEachCard * i
            this.handCards[i].setPosition(x, 0)
            this.handCards[i].zIndex = i
        }
    }
}
