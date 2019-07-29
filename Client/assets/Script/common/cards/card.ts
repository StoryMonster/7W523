

export default class Card extends cc.Node
{
    protected value: number = 0
    protected view: cc.Sprite = null

    constructor(value: number)
    {
        super()
        this.setContentSize(new cc.Size(80, 100))
        this.setScale(0.5, 0.5)
        this.value = value
        this.name = `card-${value}`
        this.view = this.addComponent(cc.Sprite)
        this.view.spriteFrame = new cc.SpriteFrame(cc.url.raw(`resources/cards/${value}.png`))
    }

    setPosition(x: number, y: number)
    {
        this.x = x
        this.y = y
    }

    getValue(): number
    {
        return this.value
    }
}