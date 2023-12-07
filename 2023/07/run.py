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

CARD_VALUES_JOKER = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 0,
}

class Hand:
    def __init__(self, cards, jokers=False):
        # self.cards = cards
        # self.cards = cards
        self.card_values = Hand.get_values(cards, jokers)
        self.best_card_values = Hand.get_best_combination(self.card_values)
        # self.best_card_values = Hand.get_values(self.best_combo, jokers)
        # self.hand_value = Hand.find_type(self.card_values)
        self.hand_value = Hand.find_type(self.best_card_values, jokers)

    @staticmethod
    def get_values(cards, jokers=False):
        assert isinstance(cards, str)
        if jokers:
            return [CARD_VALUES_JOKER[card] for card in cards]
        else:
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
    def find_type(card_values, jokers=False):
        if jokers:
            card_values = Hand.get_best_combination(card_values)

        return Hand._find_type(card_values)
        
    # @staticmethod
    # def _find_type_with_jokers(cards):
    #     cards = Hand.get_best_combination(cards)
    #     return Hand._find_type(cards)
                
    @staticmethod
    def get_best_combination(input_card_values):
        assert isinstance(input_card_values, list)
        assert isinstance(input_card_values[0], int)
        
        card_values = input_card_values.copy()

        # cards = sorted(cards)
        best_combo = card_values.copy()
        max_type = 0
        # joker = False
        for i in range(len(card_values)):
            # if card is joker
            if card_values[i] == 0:
                # joker = True
                # try all combinations
                # max_type = 0
                for value in range(2, 14):
                    card_values[i] = value
                    # print(f"{card_values = }")
                    combo = Hand.get_best_combination(card_values)
                    hand_type = Hand._find_type(combo)
                    if hand_type > max_type:
                        max_type = hand_type
                        best_combo = combo.copy()

        return best_combo

    
    @staticmethod
    def _find_type(cards):
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
    def __init__(self, line, jokers=False):
        self.line = line
        self.hand, self.bid = Bid.parse_line(line, jokers)
        self.rank = None
    
    @staticmethod
    def parse_line(line, jokers=False):
        cards, bid = line.split(" ")
        bid = int(bid)
        return Hand(cards, jokers), bid

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


def star2(filename):
    lines = get_input(filename)
    
    bids = [Bid(line, jokers=True) for line in lines]
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
    # print(kk.card_values)
    # print(kk.hand_value)
    kt = Hand("KTJJT")
    # print(kt.card_values)
    assert kt < kk
    
    # hand = Hand("2222J")
    # assert hand.hand_value == 6
    
    assert Hand.get_best_combination([2,2,2,2,2]) == [2,2,2,2,2]
    assert Hand.get_best_combination([12,12,12,12,12]) == [12,12,12,12,12]
    assert Hand.get_best_combination([2,3,4,5,6]) == [2,3,4,5,6]
    assert Hand.get_best_combination([2,2,2,2,0]) == [2,2,2,2,2]
    assert Hand.get_best_combination([0,2,2,2,0]) == [2,2,2,2,2]
    assert Hand.get_best_combination([2,2,2,0,0]) == [2,2,2,2,2]
    assert Hand.get_best_combination([0,0,0,0,0]) == [2,2,2,2,2]
    
    assert Hand.find_type([2,2,2,2,2]) == 6
    assert Hand.find_type([2,2,2,2,0], jokers=True) == 6
    
    # hand = Hand("2222J", jokers=True)
    # assert hand.hand_value == 6
    
    # lines = get_input("example.txt")
    # bids = [Bid(line) for line in lines]
    # bids = sorted(bids)
    # assert bids[0] == Bid("5H 5")
    
    ktjjt = Hand("KTJJT", jokers=True)
    assert ktjjt.hand_value == 5
    # print(f"{ktjjt.card_values = }")
    # print(f"get values: {Hand.get_values('KTJJT', jokers=True)}")
    assert ktjjt.card_values == ([CARD_VALUES_JOKER[card] for card in "KTJJT"])
    
    qqqja = Hand("QQQJA", jokers=True)
    assert qqqja.hand_value == 5
    # print(f"{qqqja.card_values = }")
    
    assert qqqja < ktjjt
    
    t55j5 = Hand("T55J5", jokers=True)
    assert t55j5.hand_value == 5
    # print(f"{t55j5.card_values = }")
    
    assert t55j5 < qqqja
    
    h32t3k = Hand("32T3K", jokers=True)
    assert h32t3k.hand_value == 1
    
    kk677 = Hand("KK677", jokers=True)
    assert kk677.hand_value == 2
    
    assert h32t3k < kk677
    assert kk677 < t55j5
    
    lines = get_input("example.txt")
    bids = [Bid(line, jokers=True) for line in lines]
    bids = sorted(bids)
    
    for bid in bids:
        print(bid.line)
    assert bids[0].line == "32T3K 765"
    
    jjjjj = Hand("JJJJJ", jokers=True)
    assert jjjjj.hand_value == 6
    
    assert h32t3k < jjjjj
    
    jjjjq = Hand("JJJJQ", jokers=True)
    assert jjjjq.best_card_values == [11,11,11,11,11]
    print(f"{jjjjq.best_card_values = }")
    print(f"{jjjjq.card_values = }")
    print(f"{jjjjq.hand_value = }")
    assert jjjjq.hand_value == 6
    # assert jjjjq < jjjjj
    
    


if __name__ == "__main__":
    hand = Hand("JJJQQ", jokers=True)
    assert hand.hand_value == 6
    
    tests()

    example = star1("example.txt")
    print(f'Example: {example}')
    assert(example == 6440)
    
    print(f'First star: {star1("input.txt")}')
    # assert(star1("input.txt") == 6209190)
    
    # print(f'Second star: {star1("input.txt")}')
    
    example = star2("example.txt")
    print(f"Star 2 example {example}")
    assert(example == 5905)

    print(f'Second star: {star2("input.txt")}')
    
    # 251884819 too high
    # 251824095