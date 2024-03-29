import numpy as np
import scipy.io as sio

from collections.abc import Iterable

from .data_game import DataGame
from .enums import Outcome, Move
from .progress_bar import ProgressBar


class Generate():
    '''
    Creates and stores data in this format:
    y = | WIN/TIE/LOSS |
    X = | Hit/Stand | dealer_card | pre_hit_hand_value | player_aces |
        2s | 3s |4s | 5s | 6s | 7s | 8s | 9s | 10JQKs | As |
    '''
    data_row_num_elem = 14

    def __init__(self):
        self.data_file = './logistic_regression/blackjack_data.mat'
        self.result = []
        self.data = []
        self.game = None

    def run(self):
        self.play()
        result_np = np.array(self.result, dtype=np.double).reshape(-1, 1)
        data_np = np.array(
            self.data, dtype=np.double).reshape(-1, Generate.data_row_num_elem)
        result_rows, _ = np.shape(result_np)
        data_rows, _ = np.shape(data_np)
        # print("result length {}: {}".format(len(self.result), self.result))
        # print("data length {}: {}".format(len(self.data)/13, self.data))
        # print("result_rows: {}, data_rows: {}".format(result_rows,
        #                                               data_rows))
        assert result_rows == data_rows
        sio.savemat(self.data_file, {'X': data_np, 'y': result_np})

    def play(self):
        progress_bar_prefix = 'Generate Data: '
        max_deck_len, min_deck_len = 3*52, 20
        tot_iterations = max_deck_len - min_deck_len
        rep_per_deck_len = 100
        for deck_len in range(max_deck_len, min_deck_len, -1):
            iteration = tot_iterations - deck_len + min_deck_len + 1
            self._play_rounds(iteration, tot_iterations,
                              progress_bar_prefix, rep_per_deck_len, deck_len)

    @ProgressBar.print_bar
    def _play_rounds(self, iteration, tot_iterations, prefix, repetitions,
                     deck_len):
        for iteration in range(repetitions):
            self.game = DataGame(deck_len)
            self.game.deal_initial_cards()
            for _ in range(tot_iterations):
                self._play_round()

    def _play_round(self):
        self.game.reset_initial_cards()
        self.game.deck.shuffle()

        self._action(Move.STAND)
        self._action(Move.HIT)

    def _action(self, move):
        (win, dealer_init_val, player_val_pre_last_hit,
            player_aces, cards_layout) = self.game.play(move)

        if win == Outcome.INVALID:
            return

        self._save_data(win, move.value, dealer_init_val,
                        player_val_pre_last_hit, player_aces, cards_layout)

    def _save_data(self, win, move, dealer_init_val, player_val_pre_last_hit,
                   player_val_final, cards_layout):
        self.result.append(win.value)
        self.data += self._flatten(move, dealer_init_val,
                                   player_val_pre_last_hit, player_val_final,
                                   cards_layout)

    def _flatten(self, *args):
        result = []
        for item in args:
            if isinstance(item, tuple) or isinstance(item, Iterable):
                result += [elem for elem in item]
            else:
                result.append(item)

        return result
