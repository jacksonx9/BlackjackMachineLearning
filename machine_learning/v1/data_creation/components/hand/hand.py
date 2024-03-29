class Hand():
    def __init__(self):
        self.cards = []

    def __repr__(self):
        class_name = type(self).__name__
        return '{}('.format(class_name) + ','.join(str(card) for card in
                                                   self.cards) + ')'

    def __str__(self):
        return ','.join(str(card) for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        self.cards.pop()

    def num_aces(self):
        return sum(1 for c in self.cards if c.ace())

    def value(self):
        '''Calculate the value of the hand. Aces can be 11 or 1.'''
        aces = sum(1 for c in self.cards if c.ace())
        value = sum(c.value() for c in self.cards)
        while value > 21 and aces > 0:
            aces -= 1
            value -= 10
        return value

    def blackjack(self):
        '''Determine if there are only 2 cards add to 21.'''
        return len(self.cards) == 2 and self.value() == 21

    def twenty_one(self):
        return self.value() == 21

    def bust(self):
        '''Determine if the hand is worth more than 21.'''
        return self.value() > 21
