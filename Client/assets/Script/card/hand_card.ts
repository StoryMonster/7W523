import Card from "./card"

export default class HandCard extends Card
{
    public isSelected: boolean = false

    constructor(value: number)
    {
        super(value)
        this.on(cc.Node.EventType.TOUCH_END, this.onClicked, this)
    }

    onClicked()
    {
        if (this.y != 0)
        {
            this.y = 0
            this.isSelected = false
        }
        else
        {
            this.y += 20
            this.isSelected = true
        }
    }
}
