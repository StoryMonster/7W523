import UsedCard from "./usedcard";
import CardBack from "./cardback";

export default class EnemyCardsManager
{
    private handCardsNum: number = 0
    private usedCards: UsedCard[] = []
    private handCards: CardBack[] = []
    private maxHandCardsNum: number = 5
    private handCardsNode: cc.Node = null
    private usedCardsNode: cc.Node = null

    constructor(node: cc.Node)
    {
        this.handCardsNode = node.getChildByName("handcards")
        this.usedCardsNode = node.getChildByName("playedcards")
    }

    dispatchCards()
    {
        this.clearUsedCards()
        let handCardsNum: number = this.handCards.length
        for (let i: number = handCardsNum; i < this.maxHandCardsNum; ++i)
        {
            let handcard: CardBack = new CardBack()
            this.handCardsNode.addChild(handcard)
            this.handCards.push(handcard)
        }
        this.arrageHandCards()
    }

    deal(cards: number[])
    {
        let cardsNum: number = cards.length
        if (cardsNum <= 0) { return }
        for (let card of cards)
        {
            this.removeOneHandCard()
            this.addUsedCard(card)
        }
        this.arrangeUsedCards()
        this.arrageHandCards()
    }

    pass()
    {}

    private addUsedCard(value: number)
    {
        let card: UsedCard = new UsedCard(value)
        this.usedCardsNode.addChild(card)
        this.usedCards.push(card)
    }

    private removeOneHandCard()
    {
        let cardsNum: number = this.handCards.length
        if (cardsNum <= 0) { return }
        this.handCards[0].removeFromParent()
        this.handCards.splice(0, 1)
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