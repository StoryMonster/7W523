import CardBack from "./card_back";
import HandCardManager from "./hand_card_manager";
import Card from "./card";


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
        for (let i: number = 0; i < cards.length; ++i)
        {
            this.cards[i].removeFromParent()
        }
        this.cards.splice(0, cards.length)
        this.arrangeCards()
    }

    getHandCardsNum(): number { return this.cards.length }

    setHandCards(cards: number[])
    {
        this.node.removeAllChildren()
        let handCards: Card[] = []
        for (let card of cards)
        {
            let handcard: Card = new Card(card)
            this.node.addChild(handcard)
            handCards.push(handcard)
        }
        let cardsNum: number = cards.length
        if (cardsNum <= 0) { return }
        let uncorverWidthEachCard: number = 50
        let cardWidth: number = this.cards[cardsNum - 1].getContentSize().width
        let totalWidth: number = cardWidth + uncorverWidthEachCard * (cardsNum - 1)
        let startX: number = 0 - (totalWidth/2)
        for (let i: number = 0; i < cardsNum; ++i)
        {
            let x: number = startX + uncorverWidthEachCard * i
            handCards[i].setPosition(x, 0)
            handCards[i].zIndex = i
        }
    }
}