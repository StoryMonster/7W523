import random

class CardHeap:
    def __init__(self, cards_num=54, start_index=1):
        self.cards_num = cards_num
        self.cards = [i for i in range(start_index, self.cards_num+start_index)]
        self.cardHeapIndex = 0

    def washCards(self):
        j = self.cards_num - 1
        while j > 0:
            i = random.randint(0, j)
            temp = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = temp
            j -= 1
        self.cardHeapIndex = 0

    def getCards(self, num):
        cards = []
        available_cards_num = self.cards_num - self.cardHeapIndex
        cards_num_to_take = num if num <= available_cards_num else available_cards_num
        for i in range(cards_num_to_take):
            cards.append(self.cards[self.cardHeapIndex])
            self.cardHeapIndex += 1
        return cards

    def isEmpty(self):
        return self.cardHeapIndex == self.cards_num

    def calcCardScore(self, card):
        val = card % 13
        if val == 5: return 5
        if val == 10 or val == 0: return 10
        return 0
