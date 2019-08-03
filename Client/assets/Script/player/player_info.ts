

export default class Player{
    static playerId: number = 0
    private static instance: Player = new Player()

    private constructor()
    {
    }

    static getInstance(): Player
    {
        return Player.instance
    }
}
