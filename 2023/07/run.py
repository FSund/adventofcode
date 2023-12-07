import numba
from numba import njit, int64
import concurrent.futures
import functools

def get_input(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    return lines


CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.card_values = Hand.get_values(cards)
        self.hand_value = Hand.find_type(self.card_values)

    @staticmethod
    def get_values(cards):
        assert isinstance(cards, str)
        return [CARD_VALUES[card] for card in cards]

    def __lt__(self, other):
        if self.hand_value < other.hand_value:
            return True
        elif self.hand_value > other.hand_value:
            return False
        else:
            for i in range(len(self.card_values)):
                if self.card_values[i] < other.card_values[i]:
                    return True
                elif self.card_values[i] > other.card_values[i]:
                    return False

    @staticmethod
    def find_type(cards):
        """
        Five of a kind: 6
        Four of a kind: 5
        Full house: 4
        Three of a kind: 3
        Two pair: 2
        One pair: 1
        High card: 0
        """
        cards = sorted(cards)
        # five of a kind
        if cards[0] == cards[4]:
            return 6
        # four of a kind
        elif cards[0] == cards[3] or cards[1] == cards[4]:
            return 5
        # full house
        elif (cards[0] == cards[2] and cards[3] == cards[4] 
              or cards[0] == cards[1] and cards[2] == cards[4]):
            return 4
        # three of a kind
        elif (cards[0] == cards[2] 
              or cards[1] == cards[3] 
              or cards[2] == cards[4]):
            return 3
        # two pair
        elif (cards[0] == cards[1] and cards[2] == cards[3]
              or cards[0] == cards[1] and cards[3] == cards[4]
              or cards[1] == cards[2] and cards[3] == cards[4]):
            return 2
        # one pair
        elif (cards[0] == cards[1] 
              or cards[1] == cards[2] 
              or cards[2] == cards[3] 
              or cards[3] == cards[4]):
            return 1
        else:
            return 0
        

    def __repr__(self):
        return f'{self.card_values}'

    def __str__(self):
        return f'{self.card_values}'


class Bid:
    def __init__(self, line):
        self.hand, self.bid = Bid.parse_line(line)
        self.rank = None
    
    @staticmethod
    def parse_line(line):
        cards, bid = line.split(" ")
        bid = int(bid)
        return Hand(cards), bid

    def __lt__(self, other):
        return self.hand < other.hand

    def __repr__(self):
        return f'{self.hand} {self.bid}'
    
    def __str__(self):
        return f'{self.hand} {self.bid}'


def star1(filename):
    lines = get_input(filename)
    
    bids = [Bid(line) for line in lines]
    bids = sorted(bids)
    # print(bids)
    
    sum = 0
    for i in range(len(bids)):
        rank = i + 1
        # print(f"{bids[i].bid} * {rank}")
        sum += rank * bids[i].bid
    
    return sum

def tests():
    assert Hand.get_values("32T3K") == [3, 2, 10, 3, 13]
    
    this = Hand("32T3K")
    other = Hand("32T3Q")
    assert other < this
    
    this = Bid("32T3K 1")
    other = Bid("32T3Q 1")
    assert other < this
    
    kk = Hand("KK677")
    print(kk.card_values)
    print(kk.hand_value)
    kt = Hand("KTJJT")
    print(kt.card_values)
    assert kt < kk
    
    # lines = get_input("example.txt")
    # bids = [Bid(line) for line in lines]
    # bids = sorted(bids)
    # assert bids[0] == Bid("5H 5")


if __name__ == "__main__":
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 6440)
    
    print(f'First star: {star1("input.txt")}')
    # assert(star1("input.txt") == 6209190)
    
    # print(f'Second star: {star2("input.txt")}')
    # assert(star2("input.txt") == 28545089)
