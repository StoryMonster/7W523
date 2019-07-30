import random

class CardHeap:
    def __init__(self, cards_num=54, start_index=1):
        self.cards_num = 54
        self.cards = [i for i in range(start_index, self.cards_num+start_index)]
        self.unused_card_start_index = 0

    def washCards(self):
        j = self.cards_num - 1
        while j > 0:
            i = random.randint(0, j)
            temp = self.cards[i]
            self.cards[i] = self.cards[j]
            self.cards[j] = temp
            j -= 1
        self.unused_card_start_index = 0

    def getCards(self, num):
        cards = []
        available_cards_num = self.cards_num - self.unused_card_start_index
        cards_num_to_take = num if num <= available_cards_num else available_cards_num
        for i in range(cards_num_to_take):
            cards.append(self.cards[self.unused_card_start_index])
            self.unused_card_start_index += 1
        return cards

    def isEmpty(self):
        return self.unused_card_start_index == self.cards_num