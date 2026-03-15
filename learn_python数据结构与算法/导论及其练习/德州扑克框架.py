import random
import itertools
from collections import Counter

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [f"{rank} of {suit}" for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def burn_card(self):
        self.cards.pop()

class Player:
    def __init__(self, name, chips):
        self.name = name
        self.chips = chips
        self.hand = []
        self.is_active = True
        self.is_folded = False
        self.current_bet = 0

    def get_action(self, current_bet, pot_total):
        # 简单AI：总是call
        return 'call', current_bet

class Pot:
    def __init__(self):
        self.total = 0

    def add(self, amount):
        self.total += amount

class TexasHoldemGame:
    def __init__(self, player_names, initial_chips=1000):
        self.deck = Deck()  # 复用之前的Deck类
        self.deck.shuffle()
        self.players = [Player(name, initial_chips) for name in player_names]
        self.community_cards = []
        self.pot = Pot()
        self.blind_small = 5
        self.blind_big = 10
        self.current_bet = 0
        self.game_phase = 'preflop'  # 阶段: preflop, flop, turn, river, showdown

    def deal_hole_cards(self):
        """给每位玩家发两张底牌"""
        for player in self.players:
            player.hand = [self.deck.deal() for _ in range(2)]

    def deal_flop(self):
        """发翻牌（三张公共牌）"""
        self.deck.burn_card()  # 销一张牌
        self.community_cards.extend([self.deck.deal() for _ in range(3)])
        self.game_phase = 'flop'

    def deal_turn(self):
        """发转牌"""
        self.deck.burn_card()
        self.community_cards.append(self.deck.deal())
        self.game_phase = 'turn'

    def deal_river(self):
        """发河牌"""
        self.deck.burn_card()
        self.community_cards.append(self.deck.deal())
        self.game_phase = 'river'

    def betting_round(self, start_player_index):
        """进行一轮下注"""
        active_players = [p for p in self.players if p.is_active and not p.is_folded]
        for player in active_players:
            action, amount = player.get_action(self.current_bet, self.pot.total)
            self.process_action(player, action, amount)

    def process_action(self, player, action, amount):
        if action == 'fold':
            player.is_folded = True
        elif action == 'call':
            to_call = self.current_bet - player.current_bet
            player.chips -= to_call
            self.pot.add(to_call)
            player.current_bet += to_call
        elif action == 'raise':
            to_call = self.current_bet - player.current_bet
            raise_amount = amount - self.current_bet
            player.chips -= to_call + raise_amount
            self.pot.add(to_call + raise_amount)
            player.current_bet += to_call + raise_amount
            self.current_bet = amount

    def players_remaining(self):
        return sum(1 for p in self.players if not p.is_folded)

    def showdown(self):
        print("Showdown:")
        for player in self.players:
            if not player.is_folded:
                hand_type, cards, score = HandEvaluator.evaluate_hand(player.hand, self.community_cards)
                print(f"{player.name}: {hand_type}, {list(cards)}")
        active = [p for p in self.players if not p.is_folded]
        if active:
            winner = max(active, key=lambda p: HandEvaluator.evaluate_hand(p.hand, self.community_cards)[2])
            print(f"Winner: {winner.name}")

    def run_hand(self):
        """运行一手牌的全流程"""
        self.deal_hole_cards()
        print("Hole cards dealt.")
        for player in self.players:
            print(f"{player.name}: {player.hand}")
        self.betting_round(start_player_index=2)
        if self.players_remaining() > 1:
            self.deal_flop()
            print(f"Flop: {self.community_cards}")
            self.betting_round(start_player_index=0)
        if self.players_remaining() > 1:
            self.deal_turn()
            print(f"Turn: {self.community_cards}")
            self.betting_round(start_player_index=0)
        if self.players_remaining() > 1:
            self.deal_river()
            print(f"River: {self.community_cards}")
            self.betting_round(start_player_index=0)
        if self.players_remaining() > 1:
            self.showdown()

class HandEvaluator:
    # 牌型常量
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

    @staticmethod
    def evaluate_hand(hole_cards, community_cards):
        all_cards = hole_cards + community_cards
        best_score = -1
        best_hand_type = None
        best_five_cards = None

        # 生成所有5张牌组合
        for combo in itertools.combinations(all_cards, 5):
            score, hand_type, key_cards = HandEvaluator._score_five_cards(combo)
            if score > best_score:
                best_score = score
                best_hand_type = hand_type
                best_five_cards = combo
        return best_hand_type, best_five_cards, best_score

    @staticmethod
    def _score_five_cards(five_cards):
        rank_values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14}
        ranks = []
        suits = []
        for card in five_cards:
            rank, suit = card.split(' of ')
            ranks.append(rank_values[rank])
            suits.append(suit)
        ranks.sort(reverse=True)
        is_flush = len(set(suits)) == 1
        is_straight = all(ranks[i] - ranks[i+1] == 1 for i in range(4)) or (ranks == [14,5,4,3,2])
        if is_flush and is_straight:
            if ranks[0] == 14 and ranks[1] == 13:
                score = HandEvaluator.ROYAL_FLUSH * 1000000 + sum(ranks)
                return score, HandEvaluator.ROYAL_FLUSH, ranks
            else:
                score = HandEvaluator.STRAIGHT_FLUSH * 1000000 + sum(ranks)
                return score, HandEvaluator.STRAIGHT_FLUSH, ranks
        if is_flush:
            score = HandEvaluator.FLUSH * 1000000 + sum(ranks)
            return score, HandEvaluator.FLUSH, ranks
        if is_straight:
            score = HandEvaluator.STRAIGHT * 1000000 + sum(ranks)
            return score, HandEvaluator.STRAIGHT, ranks
        count = Counter(ranks)
        counts = sorted(count.values(), reverse=True)
        if counts == [4,1]:
            score = HandEvaluator.FOUR_OF_A_KIND * 1000000 + sum(ranks)
            return score, HandEvaluator.FOUR_OF_A_KIND, ranks
        if counts == [3,2]:
            score = HandEvaluator.FULL_HOUSE * 1000000 + sum(ranks)
            return score, HandEvaluator.FULL_HOUSE, ranks
        if counts == [3,1,1]:
            score = HandEvaluator.THREE_OF_A_KIND * 1000000 + sum(ranks)
            return score, HandEvaluator.THREE_OF_A_KIND, ranks
        if counts == [2,2,1]:
            score = HandEvaluator.TWO_PAIR * 1000000 + sum(ranks)
            return score, HandEvaluator.TWO_PAIR, ranks
        if counts == [2,1,1,1]:
            score = HandEvaluator.ONE_PAIR * 1000000 + sum(ranks)
            return score, HandEvaluator.ONE_PAIR, ranks
        score = HandEvaluator.HIGH_CARD * 1000000 + sum(ranks)
        return score, HandEvaluator.HIGH_CARD, ranks

# 测试代码
if __name__ == "__main__":
    game = TexasHoldemGame(['Alice', 'Bob', 'Charlie'], 1000)
    game.run_hand()
    print("Game over.")
