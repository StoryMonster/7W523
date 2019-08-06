import HandCardManager from "../../card/hand_card_manager"
import EnemyHandCardManager from "../../card/enemy_hand_card_manager"
import PlayerHandCardManager from "../../card/player_hand_card_manager"
import AbandonCardManager from "../../card/abandon_card_manager"


export default class PlayerInRoom
{
    score: number = 0
    playerId: number = 0
    index: number = 0
    handCardMngr: HandCardManager = null
    abandonCardMngr: AbandonCardManager = null
    lastThrownCardsInRound: number[] = []
    node: cc.Node = null

    constructor(isEnemy: boolean, node: cc.Node)
    {
        this.node = node
        if (isEnemy)
        {
            this.handCardMngr = new EnemyHandCardManager(node.getChildByName("handcards"))
        }
        else
        {
            this.handCardMngr = new PlayerHandCardManager(node.getChildByName("handcards"))
        }
        this.abandonCardMngr = new AbandonCardManager(node.getChildByName("playedcards"))
        this.hideScore()
        this.hideStatus()
    }

    ready(isReady: boolean)
    {
        if (isReady)
        {
            this.node.getChildByName("status").getComponent(cc.Label).string = "准备"
            return
        }
        this.node.getChildByName("status").getComponent(cc.Label).string = ""
        this.lastThrownCardsInRound = []
    }

    deal(cards: number[])
    {
        this.handCardMngr.deal(cards)
        this.abandonCardMngr.abandonCards(cards)
        this.lastThrownCardsInRound = cards
    }

    pass()
    {
        this.node.getChildByName("status").getComponent(cc.Label).string = "不要"
        this.lastThrownCardsInRound = []
    }

    dispatchCards(cards: number[])
    {
        this.node.getChildByName("status").getComponent(cc.Label).string = ""
        this.handCardMngr.dispatchCards(cards)
        this.abandonCardMngr.clear()
        this.lastThrownCardsInRound = []
    }

    sitdown(playerId: number, index: number)
    {
        this.playerId = playerId
        this.index = index
    }

    situp()
    {
        this.playerId = 0
        this.score = 0
        this.index = 0
        this.hideScore()
        this.hideStatus()
    }

    hideScore()
    {
        this.node.getChildByName("score").getComponent(cc.Label).string = ""
    }

    hideStatus()
    {
        this.node.getChildByName("status").getComponent(cc.Label).string = ""
    }

    updateScore()
    {
        this.node.getChildByName("score").getComponent(cc.Label).string = `分数：${this.score}`
    }

    isPlayerSitting(): boolean
    {
        // 判断是否有玩家坐在此处
        return this.playerId != 0
    }

    setDealTrun(canDeal: boolean)
    {
        // 此功能仅仅适用于player1
        this.node.getChildByName("deal").active = canDeal
        this.node.getChildByName("pass").active = canDeal
    }
}