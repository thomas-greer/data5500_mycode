from DeckOfCards import *

def hand_score(hand):
    total = 0
    ace_count = 0
    for card in hand:
        total += card.val
        if card.face == "Ace":
            ace_count += 1

    while total > 21 and ace_count > 0:
        total -= 10
        ace_count -= 1

    return total


def deal_starting_hands(deck):
    user_hand = []
    dealer_hand = []
    user_hand.append(deck.get_card())
    user_hand.append(deck.get_card())
    dealer_hand.append(deck.get_card())
    dealer_hand.append(deck.get_card())
    return user_hand, dealer_hand

def print_user_hand(user_hand):
    for i, card in enumerate(user_hand, start=1):
        print(f"Card number {i} is: {card.face} of {card.suit}")

def user_turn(deck, user_hand):
    print_user_hand(user_hand)
    user_score = hand_score(user_hand)
    print(f"\nYour total score is: {user_score}")

    while True:
        if user_score > 21:
            return user_hand, user_score, True

        choice = input("Would you like a hit?(y/n) ").strip().lower()
        if choice != "y":
            break

        user_hand.append(deck.get_card())
        card_num = len(user_hand)
        new_card = user_hand[-1]
        print(f"\nCard number {card_num} is: {new_card.face} of {new_card.suit}")
        user_score = hand_score(user_hand)
        print(f"\nYour total score is: {user_score}")

    return user_hand, user_score, (user_score > 21)


def dealer_turn(deck, dealer_hand):
    print(f"\nDealer card number 1 is: {dealer_hand[0].face} of {dealer_hand[0].suit}")
    print(f"Dealer card number 2 is: {dealer_hand[1].face} of {dealer_hand[1].suit}")
    dealer_score = hand_score(dealer_hand)
    while dealer_score < 17:
        dealer_hand.append(deck.get_card())
        card_num = len(dealer_hand)
        new_card = dealer_hand[-1]
        print(f"\nDealer hits, card number {card_num} is: {new_card.face} of {new_card.suit}")
        dealer_score = hand_score(dealer_hand)

    print(f"\nDealer score is: {dealer_score}")
    return dealer_hand, dealer_score, (dealer_score > 21)


def determine_winner(user_score, dealer_score):
    if user_score > 21:
        print("You busted, you lose!")
        return

    if dealer_score > 21:
        print("Dealer Busted, you win!!!")
        return

    if dealer_score >= user_score:
        print("Dealer score is equal or higher, you lose!")
        return

    print("Your score is higher than the dealer, you win!")


def play_round(deck):
    deck.shuffle_deck()
    user_hand, dealer_hand = deal_starting_hands(deck)
    user_hand, user_score, user_busted = user_turn(deck, user_hand)
    if user_busted:
        print("You busted, you lose!")
        return

    dealer_hand, dealer_score, dealer_busted = dealer_turn(deck, dealer_hand)
    determine_winner(user_score, dealer_score)


def main():
    print("Welcome to Black Jack!\n")
    deck = DeckOfCards()
    while True:
        play_round(deck)
        again = input("\nanother game?(y/n): ").strip().lower()
        if again != "y":
            break


main()
