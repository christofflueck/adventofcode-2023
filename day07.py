import functools
from typing import Tuple

from run_util import run_puzzle


def get_card_value(card: str) -> int:
    match card:
        case 'A':
            return 14
        case 'K':
            return 13
        case 'Q':
            return 12
        case 'J':
            return 1
        case 'T':
            return 10
        case _:
            return int(card)


NON_JOKER = 'AKQT98765432'


def get_hand_value(hand: str) -> int:
    unique_cards = set(hand)
    num_unique_cards = len(unique_cards)

    if 'J' in hand:
        return max(get_hand_value(hand.replace('J', replacement)) for replacement in NON_JOKER)
    else:
        if num_unique_cards == 1:
            return 6

        if num_unique_cards == 2:
            for card in unique_cards:
                if hand.count(card) == 4 or hand.count(card) == 1:
                    return 5
            return 4

        if num_unique_cards == 3:
            for card in unique_cards:
                if hand.count(card) == 3:
                    return 3
            return 2

        if num_unique_cards == 4:
            return 1

    return 0


def compare_hands(a: Tuple[int, str, int], b: Tuple[int, str, int]) -> int:
    (a_hand_value, a_hand, a_bid) = a
    (b_hand_value, b_hand, b_bid) = b

    if a_hand_value != b_hand_value:
        return a_hand_value - b_hand_value

    cards = zip(a_hand, b_hand)

    for a_card, b_card in cards:
        a_value = get_card_value(a_card)
        b_value = get_card_value(b_card)
        if a_value != b_value:
            return a_value - b_value

    return 0


def part_a(data: str):
    input = [row.split(' ') for row in data.split('\n')]

    hands = [(get_hand_value(card), card, int(bid)) for card, bid in input]

    winning = sorted(hands, key=functools.cmp_to_key(compare_hands))

    payout = [(index + 1) * hand[2] for (index, hand) in enumerate(winning)]

    return sum(payout)


def part_b(data):
    input = [row.split(' ') for row in data.split('\n')]

    hands = [(get_hand_value(card), card, int(bid)) for card, bid in input]

    winning = sorted(hands, key=functools.cmp_to_key(compare_hands))

    payout = [(index + 1) * hand[2] for (index, hand) in enumerate(winning)]

    return sum(payout)


def main():
    examples = [
        ("""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""", 5905, 5905)
    ]
    day = int(__file__.split('/')[-1].split('.')[0][-2:])
    run_puzzle(day, part_a, part_b, examples)


if __name__ == '__main__':
    main()
