# Thomas Povinelli
# Cards.py
# September 6, 2015
# License: CC BY-SA-NC
import random
import subprocess

class EmptyDeckError(BaseException):
    pass

class Deck (object):
    def __init__(self, decks=1, aceishigh=True):
        self.numdecks = decks
        self.aceishigh = aceishigh
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Ace"]
        self.suits = ["Diamonds", "Hearts", "Spades", "Clubs"]
        self.faces = ["Jack", "Queen", "King", "Ace"]
        self.royal = [10] + self.faces
        self.fulldeck = []
        self.winninghands = {'Royal Flush':100, "Straight Flush":90, "Four of a Kind":80, 'Full House':70,
                             "Flush":60, "Straight":50, 'Three of a Kind':40, "Two Pair": 30, "One Pair":20, "High Card":15}
        if aceishigh:
            self.cardvalues = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":11, "Queen":12, "King":13, "Ace":14}
        else:
            self.cardvalues = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":11, "Queen":12, "King":13, "Ace":1}
        for h in self.suits:
            for i in self.cards:
                self.fulldeck.append((i, h))

        for i in range(decks-1):
            self.fulldeck += self.fulldeck

        self.workingdeck = self.fulldeck[:]

    def pick_a_card(self):
        if not self.workingdeck:
            raise EmptyDeckError("There are no cards left in this deck")
        card = (random.choice(self.workingdeck))
        self.workingdeck.remove(card)
        return card

    def deal(self, number):
        if len(self.workingdeck) < number:
            raise EmptyDeckError("There are not enough cards left in this deck.")
        cards = []
        for i in range(number):
            card = self.pick_a_card()
            cards.append(card)
        return cards

    def evaluate_hand(self, hand):
        twopair = False
        onepair = False
        # Royal
        for i in hand:
            royalstraight = True
            if i[0] not in self.royal:
                royalflush = False
                royalstraight = False
                break


        # Flush
        if hand[0][1] == hand[1][1] == hand[2][1] == hand[3][1] == hand[4][1]:
            flush = True
        else:
            flush = False

        numbers = []
        for i in hand:
            numbers.append(i[0])

        snums = [self.cardvalues[i] for i in numbers]
        snums.sort()
        for i in range(len(snums)-1):
            straight = True
            try:
                if snums[i] != snums[i+1] - 1:
                    straight = False
                    break
            except Exception as e:
                pass

        if flush == True and royalstraight == True:
            royalflush = True
        else:
            royalflush = False

        if flush == True and straight == True:
            straightflush = True
        else:
            straightflush = False



        for i in numbers:
            fourofakind = False
            threeofakind = False
            couldbetwo = False
            if numbers.count(i) == 4:
                fourofakind = True
                break
            if numbers.count(i) == 3:
                threeofakind = True
                break
            if numbers.count(i) == 2:
                couldbetwo = True
                firstpair = i
                break
        if couldbetwo:
            for i in numbers:
                onepair = True
                twopair = False
                if numbers.count(i) == 2 and i != firstpair:
                    twopair = True
                    break

        fullhouse = False
        couldfull = False
        for i in numbers:
            if numbers.count(i) == 3:
                couldfull = True
                used = i
                counted = 3
                break
            if numbers.count(i) == 2:
                couldfull = True
                used = i
                counted = 2
                break

        if couldfull:
            neededvalue = 3 if counted == 2 else 2
            for i in numbers:
                if numbers.count(i) == neededvalue and i != used:
                    fullhouse = True

        maxi = 0
        for i in numbers:
            if self.cardvalues[i] > maxi:
                maxi = self.cardvalues[i]
        try:
            maxi = int(maxi)
        except:
            pass

        if royalflush:
            return "Royal Flush"
        if straightflush:
            return "Straight Flush"
        if fourofakind:
            return "Four of a Kind"
        if fullhouse:
            return "Full House"
        if flush:
            return "Flush"
        if straight:
            return "Straight"
        if threeofakind:
            return "Three of a Kind"
        if twopair:
            return "Two Pair"
        if onepair:
            return "One Pair"
        return maxi

    def breakTie(self, h1, h2):
        numbers1 = []
        numbers2 = []
        eval_h1 = self.evaluate_hand(h1)
        eval_h2 = self.evaluate_hand(h2)
        for i in h1:
            numbers1.append(self.cardvalues[i[0]])

        for i in h2:
            numbers2.append(self.cardvalues[i[0]])

        numbers1.sort()
        numbers2.sort()
        if h1 == 'Royal Flush' and h2 == 'Royal Flush':
            return 'Tie', 0

        if h1 == "Straigth Flush" or h1 == "Flush" or h1 == "Straight":
            if numbers1[-1] > numbers2[-1]:
                return "First Hand", eval_h1
            elif numbers1[-1] == numbers2[-1]:
                return "Tie", 0
            else:
                return "Second Hand", eval_h2
        if self.evaluate_hand(h1) == 'Full House':

            if numbers1[0] == numbers1[1] == numbers1[2]:
                h1s = 1
            else:
                h1s = 4
            if numbers2[0] == numbers2[1] == numbers2[2]:
                h2s = 1
            else:
                h2s = 4 # you must compare either the first 3 or last 3 cards which will vary by size when sorted
            if numbers1[h1s] > numbers2[h2s] :
                return "First Hand", eval_h1
            elif numbers1[h1s] == numbers2[h2s] :
                if numbers1[-h1s] > numbers2[-h2s]  : # by using the negative you choose the end if it was the beginning or the beginning if it was the end i.e. list[1] = list[-4] list[4] = list[-1] when length is five
                    return "First Hand", eval_h1
                elif numbers1[-h1s] == numbers2[-h2s]  :
                    return "Tie", 0
                elif numbers1[-h1s] < numbers2[-h2s] :
                    return "Second Hand", eval_h2
            elif numbers1[h1s] < numbers2[h2s] :
                return "Second Hand", eval_h2
        return "Tie", 0

    def choosewinner(self, hand, hand2):
        h1 = self.evaluate_hand(hand)
        h2 = self.evaluate_hand(hand2)
        try:
            if self.winninghands[self.evaluate_hand(hand)] > self.winninghands[self.evaluate_hand(hand2)]:
                return "First hand", h1
            elif self.winninghands[self.evaluate_hand(hand)] == self.winninghands[self.evaluate_hand(hand2)]:
                return self.breakTie(hand, hand2)
            else:
                return "Second hand", h2
        except Exception as e:
            try:
                if h1 > h2:
                    return "First hand", h1
                elif h1 < h2:
                    return "Second hand", h2
                else:
                    return "Tie", 0
            except Exception as e:
                if isinstance(h1, str):
                    return "First hand", h1
                else:
                    return "Second hand", h2

    def fold(self, hand):
        if isinstance(hand, tuple):
            hand = [hand]
        for i in hand:
            self.workingdeck.append(i)

    def print_hand(self, hand, name=None):
        if isinstance(hand, tuple):
            hand = [hand]
        print("Hand - ", end=" ")
        if name:
            print(name)
        else:
            print()
        for i in hand:
            print("The {} of {}".format(i[0], i[1]))

    def show_hand(self, hand, name=None):
        if isinstance(hand, tuple):
            hand = [hand]
        print("Hand - ", end=' ')
        if name:
            print(name)
        else:
            print()
        for i in hand:
            faces = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":"J", "Queen":"Q", "King":"K", "Ace":"A"}
            suit = {"Diamonds":"⬥", "Hearts":"♥︎", "Spades":"♠︎", "Clubs":"♣︎"}
            print("{}{}".format(faces[i[0]], suit[i[1]]), end=" ")
        print()

    def exchange_cards(self, hand, money, name=None):

        print("Exchange cards for the your hands")
        #self.show_hand(hand, name)
        nums = input("Enter the number of the cards to exchange\n"
                     "Starting with 1 ending with 5 (0 to hold): ")
        nums = nums.strip()
        if nums == "0":
            return hand
        numbers = nums.split(' ')
        try:
            numbers = [int(x) - 1 for x in numbers]
        except:
            return 1
        for i in numbers:
            self.fold(hand[i])
            hand.remove(hand[i])
            newcard = self.pick_a_card()
            hand.insert(i, newcard)
        return hand

    def replenishdeck(self):
        self.__init__(self.numdecks, self.aceishigh)

    def addDeck(self):
        self.workingdeck.extend(self.fulldeck.copy())

def main():
    cont = False
    input("Welcome to Texas Hold Em. Press enter to start_ ")
    deck = Deck(3)
    name = input("Enter your name: ")
    money = 10000
    while not cont:
        usr = deck.deal(5)
        cpu = deck.deal(5)
        print("Here is your hand")
        deck.show_hand(usr)
        bet = int(input("Total funds: %i\nenter a bet (1 - 5): " % money))
        deck.exchange_cards(usr, name)

        winner, winning = deck.choosewinner(usr, cpu)
        amount = deck.winninghands.get(winning, winning) * bet
        if winner == 'Second hand':
            print("You lose. CPU had %s" % winning)
            print("You: ", end=''); deck.show_hand(usr, name)
            print("CPU: ", end=''); deck.show_hand(cpu, "CPU")
            money -= amount
            print("you lost: $%i" % amount)

        elif winner == 'First hand':
            print("You won. You had %s" % winning)
            print("You: ", end=''); deck.show_hand(usr, name)
            print("CPU: ", end=''); deck.show_hand(cpu, "CPU")
            money += amount
            print("you won: $%i" % amount)
        elif winner == "Tie":
            print("Tie")
            print("You: ", end=''); deck.show_hand(usr, name)
            print("CPU: ", end=''); deck.show_hand(cpu, "CPU")
            print("You won $0")
        deck.fold(usr)
        deck.fold(cpu)
        if money <= 0:
            print("You ran out of money!")
            print("Game over")
            break

        cont = input("Enter to play again or 'quit' to quit: ")
        subprocess.call('clear')

if __name__ == "__main__":
    main()
#deck = Deck()
##print(deck.workingdeck)
#
#
#d = deck.deal(5)
#f = deck.deal(5)
#deck.show_hand(d, 1)
#deck.show_hand(f, 2)
#deck.exchange_cards(d)
#deck.exchange_cards(f)
#deck.show_hand(d, 1)
#deck.show_hand(f, 2)
#print(deck.choosewinner(d, f))
#deck.fold(d)
#deck.fold(f)
#print()
