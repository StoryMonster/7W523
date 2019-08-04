
export default class PlayerInfoInRoom
{
    public playerId: number = 0
    public index: number = 0
    public score: number = 0
    public cards: number[] = []
    public isReady: boolean = false
    public isPassing: boolean = false
    public generalInfo: string = ""
    private node: cc.Node = null
    private cardsManager: CardsManager = null

    constructor(cardsManager: CardsManager, node: cc.Node)
    {
        this.cardsManager = cardsManager
        this.node = node
    }

    setReady(isReady: boolean)
    {
        this.isReady = isReady
        if (this.isReady) {
            this.node.getChildByName("status").getComponent(cc.Label).string = "准备"
        }
        else{
            this.node.getChildByName("status").getComponent(cc.Label).string = ""
        }
    }

    deal(cards: number[])
    {
        this.cardsManager.deal(cards)
    }

    dispatchCards(cards: number[])
    {
        this.cardsManager.dispatchCards(cards)
    }

    getHandCardsNum(): number
    {
        return this.cardsManager.getHandCardsNum()
    }

    getSelectedCards(): number[]
    {
        return this.cardsManager.getSelectHandCards()
    }

    sitdown()
    {
        this.generalInfo = `${this.playerId}`
    }

    situp()
    {
        this.cards = []
        this.playerId = 0
        this.index = 0
        this.score = 0
        this.isReady = false
        this.isPassing = false
        this.generalInfo = ""
        this.node.getChildByName("score").getComponent(cc.Label).string = ""
        this.setReady(false)
    }

    setPass(toPass: boolean)
    {
        this.isPassing = toPass
        if (this.isPassing) {
            this.node.getChildByName("status").getComponent(cc.Label).string = "不要"
        }
        else{
            this.node.getChildByName("status").getComponent(cc.Label).string = ""
        }
    }

    setScore(score: number = 0)
    {
        this.score = score
        this.node.getChildByName("score").getComponent(cc.Label).string = `分数: ${this.score}`
    }

    setHandCards(cards: number[])
    {
        this.cards = cards
        this.cardsManager.setHandCards(cards)
    }
}
