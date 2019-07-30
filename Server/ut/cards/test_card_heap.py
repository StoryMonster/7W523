import pytest
from cards.card_heap import CardHeap

@pytest.fixture
def cardheap():
    instance = CardHeap(54, 1)
    return instance

def test_get_cards(cardheap):
    cardheap.washCards()
    cards = cardheap.getCards(3)
    assert(len(cards) == 3)
    assert(not cardheap.isEmpty())
    cards = cardheap.getCards(12)
    assert(len(cards) == 12)
    assert(not cardheap.isEmpty())
    cards = cardheap.getCards(9)
    assert(len(cards) == 9)
    assert(not cardheap.isEmpty())
    cards = cardheap.getCards(35)
    assert(len(cards) == 30)
    assert(cardheap.isEmpty())
