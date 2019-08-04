import Card from "./card"

export default class HandCard extends Card
{

    constructor(value: number)
    {
        super(value)
        this.on(cc.Node.EventType.TOUCH_END, this.select, this)
    }

    select()
    {
        if (this.y != 0)
        {
            this.y = 0
        }
        else
        {
            this.y += 20
        }
    }

    isSelected(): boolean
    {
        return this.y != 0
    }
}
