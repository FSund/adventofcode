from typing import Self

def get_score(line):
    line = line.split(": ")[1]
    numbers, winning = line.split(" | ")
    numbers = numbers.split()
    winning = winning.split()
    
    score = 0
    for number in numbers:
        if number in winning:
            if score:
                score = score * 2
            else:
                score = 1

    return score


def main(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    
    points = 0
    for line in lines:
        points += get_score(line)
    
    return points
    


# def get_matches(line, cards):
#     card, line = line.split(": ")[1]
#     card = card.strip("Card ")
#     left, right = line.split(" | ")
#     left = left.split()
#     right = right.split()
    
#     matches = []
#     for number in left:
#         if number in right:
#             matches.append()

#     return matches

def count_matches(left, right):
    matches = 0
    for number in left:
        if number in right:
            matches += 1
    
    return matches


def get_copies(line, cards, card_count, parent=None):
    card, line = line.split(": ")[1]
    card = card.strip("Card ")
    left, right = line.split(" | ")
    left = left.split()
    right = right.split()
    
    n_matches = count_matches(left, right)
    if parent:
        for i in range(1, n_matches+1):
            if i < len(card_count):
                card_count[i] += 1
    else:
        get_copies()
    
    # card_count[parent] += get_copies()


class Card:
    def __init__(self, line):
        id = line.split(": ")[0]
        id = id.strip("Card ")
        id = int(id)
    
        self.count = 0
        self.id = id
        self.line = line
        self.n_matches = self._count_matches(line)

    @staticmethod
    def _count_matches(line):
        line = line.split(": ")[1]
        left, right = line.split(" | ")
        left = left.split()
        right = right.split()
        
        n_matches = 0
        for number in left:
            if number in right:
                n_matches += 1
        
        return n_matches

    def win(self, cards: dict[Self]):
        self.count += 1
        
        # if self.id == 5:
        #     print(f"loop: {list(range(self.id + 1, self.id + 1 + self.n_matches))}")

        for i in range(self.id + 1, self.id + 1 + self.n_matches):
            if i in cards.keys():
                cards[i].win(cards)


def star2(filename):
    lines = []
    with open(filename) as file:
        for line in file:
            lines.append(line.strip("\n"))
    
    cards = {}
    for line in lines:
        id = line.split(": ")[0]
        id = id.strip("Card ")
        id = int(id)
        cards[id] = Card(line)
    
    for key, card in cards.items():
        card.win(cards)
        
    count = 0
    for key, card in cards.items():
        # print(f"Card: {card.id} count: {card.count}")
        count += card.count
    
    return count


def tests():
    card = Card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert card.n_matches == 4
    
    card = Card("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19")
    assert card.n_matches == 2
    
    card = Card("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1")
    assert card.n_matches == 2
    
    card = Card("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83")
    assert card.n_matches == 1

    card = Card("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36")
    assert card.n_matches == 0
    
    card = Card("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11")
    assert card.n_matches == 0


if __name__ == "__main__":
    example = main("example.txt")
    assert(example == 13)
    print(f'Example: {example}')
    
    print(f'First star: {main("input.txt")}')
    # assert(star1("input.txt") == 530495)
    
    tests()
    example = star2("example.txt")
    assert example == 30
    print(f'Example: {example}')
    
    s2 = star2("input.txt")
    assert s2 == 23806951
    print(f'Second star: {s2}')
