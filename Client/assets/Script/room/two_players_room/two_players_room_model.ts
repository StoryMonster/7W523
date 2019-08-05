import PlayerInRoom from "./player_in_room";
import {GameResult} from "../../common/game_result"


export default class TwoPlayersRoomModel
{
    private p1: PlayerInRoom = null
    private p2: PlayerInRoom = null
    p2LatestCards: number[] = []

    constructor(p1Node: cc.Node, p2Node: cc.Node)
    {
        this.p1 = new PlayerInRoom(false, p1Node)
        this.p2 = new PlayerInRoom(true, p2Node)
    }

    isPlayer2Exist(): boolean
    {
        return this.p2.isPlayerSitting()
    }

    dispatchCards(p1Cards: number[], p2Cards: number[])
    {
        this.p1.dispatchCards(p1Cards)
        this.p2LatestCards = []
        this.p2.dispatchCards(p2Cards)
    }

    deal(playerId: number, cards: number[])
    {
        if (playerId == this.p1.playerId)
        {
            this.p1.deal(cards)
        } else if (playerId == this.p2.playerId)
        {
            this.p2.deal(cards)
            this.p2LatestCards = cards
        }
    }

    pass(playerId: number)
    {
        if (playerId == this.p1.playerId)
        {
            this.p1.pass()
        } else if (playerId == this.p2.playerId)
        {
            this.p2.pass()
        }
    }

    changeDealOwner(playerId: number)
    {
        this.p1.setDealTrun(playerId == this.p1.playerId)
    }

    player2SitDown(playerId: number, index: number)
    {
        this.p2.sitdown(playerId, index)
    }

    player1SitDown(playerId: number, index: number)
    {
        this.p1.sitdown(playerId, index)
    }

    player2SitUp()
    {
        this.p2.situp()
    }

    gamestart()
    {
        this.p1.updateScore()
        this.p2.updateScore()
        this.p1.hideStatus()
        this.p2.hideStatus()
    }

    gameover()
    {
        this.p1.hideStatus()
        this.p2.hideStatus()
    }

    changePlayerScore(playerId: number, score: number)
    {
        if (playerId == this.p1.playerId)
        {
            this.p1.score = score
            this.p1.updateScore()
        } else if (playerId == this.p2.playerId)
        {
            this.p2.score = score
            this.p2.updateScore()
        }
    }

    getGameResult(): GameResult
    {
        if (this.p1.score > this.p2.score)
        {
            return GameResult.Win
        } else if (this.p1.score < this.p2.score)
        {
            return GameResult.Fail
        }
        return GameResult.Draw
    }

    ready(playerId: number, isReady: boolean)
    {
        if (playerId == this.p1.playerId)
        {
            this.p1.ready(isReady)
        } else if (playerId == this.p2.playerId)
        {
            this.p2.ready(isReady)
        }
    }

    getP2HandCardsNum(): number
    {
        return this.p2.handCardMngr.getHandCardsNum()
    }

    getPlayer1SelectedCards(): number[]
    {
        return this.p1.handCardMngr.getSelectedHandCards()
    }
}