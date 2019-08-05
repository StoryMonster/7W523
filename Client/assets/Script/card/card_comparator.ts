

export default class CardComparator
{
    static getCardsLevel(cards: number[]): number
    {
        let len: number = cards.length
        if (len == 1) { return 1 }
        if (len == 2 && ((cards[0] == 53 && cards[1] == 54) || (cards[0] == 54 && cards[1] == 53))) { return 5 }
        for (let i: number = 1; i < cards.length; ++i)
        {
            if (cards[0] % 13 != cards[i] % 13) { return 0 }
        }
        if (len == 2) { return 2}
        if (len == 3) { return 3}
        if (len == 4) { return 4}
        return 0
    }

    static isCardTypeLeagal(cards: number[])
    {
        let len: number = cards.length
        if (len == 1) { return true }
        if (len == 2) {
            return ((cards[0] % 13) == (cards[1] % 13) || cards[0] + cards[1] == 107)   // 53+54=107, 双王
        }
        if (len == 3 || len == 4)
        {
            for (let i: number = 1; i < len; ++i)
            {
                if (cards[i] % 13 != cards[0] % 13) { return false }
            }
        }
        return true
    }

    static compare(cards1: number[], cards2: number[]): number
    {
        // 此处只做单纯两副牌大小比较，不考虑扯牌情况
        let lvl1: number = CardComparator.getCardsLevel(cards1)
        let lvl2: number = CardComparator.getCardsLevel(cards2)
        if (lvl1 == 0) { return -1}
        if (lvl2 == 0) { return 1}
        // 单牌判断
        if (lvl1 == 1 && lvl2 == 1)
        {
            let singleRankTable: number[] = [7, 54, 53, 5, 2, 3, 1, 0, 12, 11, 10, 9, 8, 6, 4]
            let val2: number = (cards2[0] >= 53) ? cards2[0] : cards2[0] % 13
            let val1: number = (cards1[0] >= 53) ? cards1[0] : cards1[0] % 13
            if (val1 == val2) { return 0 }
            for (let val of singleRankTable)
            {
                if (val == val1) { return 1 }
                if (val == val2) { return -1 }
            }
        }

        // 王炸判断
        if (lvl1 == 4 && lvl2 == 5)
        {
            return (cards1[0] % 13 == 7) ? 1 : -1
        }
        if (lvl1 == 5 && lvl2 == 4)
        {
            return (cards2[0] % 13 == 7) ? -1 : 1
        }
        // 同等牌数判断
        if (lvl1 == lvl2)
        {
            if (cards2[0] % 13 == cards1[0] % 13) { return 0 }
            let otherRankTable: number[] = [7, 5, 2, 3, 1, 0, 12, 11, 10, 9, 8, 6, 4]
            for (let val of otherRankTable)
            {
                if (val == cards2[0]%13) { return -1 }
                if (val == cards1[0]%13) { return 1 } 
            }
        }
        return lvl2 > lvl1 ? -1 : 1
    }
}