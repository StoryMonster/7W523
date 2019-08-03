

interface CardsManager{
    dispatchCards(cards: number[]): void
    deal(cards: number[]): void
    pass(): void
    getSelectHandCards(): number[]
    getHandCardsNum(): number
}
