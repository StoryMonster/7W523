

export default class CardBack extends cc.Node
{
    private view: cc.Sprite = null
    constructor()
    {
        super()
        this.setAnchorPoint(0.5, 0.5)
        this.setScale(0.5, 0.5)
        this.name = "poker_bg"
        this.view = this.addComponent(cc.Sprite)
        this.view.spriteFrame = new cc.SpriteFrame(cc.url.raw(`resources/cards/bg1.png`))
    }
}