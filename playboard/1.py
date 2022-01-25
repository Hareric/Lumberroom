#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2021, All rights reserved.
# Author: Eric <demo@flickering.ai>

"""
- 0: 1分
- 1: 5分
- 2: 1角
- 3: 5角
- 4: 1元
- 61: 袋子
"""
import numpy as np
import json
import copy
import logging
import random
import time

import requests

base_url = "http://192.168.2.233:6699"


# base_url = "https://test-api-6699.mathufo.com"


class Board:
    def __init__(self, level):
        self.height_speed = 0  # height权重每次的增速

        if level == 0:
            self.level = level
            self.board = [[0 for _ in range(5)] for _ in range(5)]
            self.score = 0
            self.height = 0
        else:
            req = requests.request('get',
                                   url=f"{base_url}/init?token=wendachen&level={level}")
            res = req.json()
            self.level = level
            self.board = res['board']
            self.score = res['score']
            self.height = res['height']
        self.connect_value = self._connect_value()
        self.total_num = self._total_num()
        self.add_score = 0
        self.origin_score = 0

    def _total_num(self):
        s = 0
        for i in self.board:
            s += len(i)
        return s

    def max_length(self):
        max_len = 0
        for i in self.board:
            if len(i) > max_len:
                max_len = len(i)
        return max_len

    def std_length(self):
        t = [len(i) for i in self.board]
        return float(np.std(t))

    def move(self, a, b):
        """
        from a to b
        """
        ...

    def print_board(self):
        for j in range(10)[1:]:
            for i in self.board:
                try:
                    print(i[-j], end=" ")
                except IndexError:
                    print(" ", end=" ")
            print()
        print(
            f"[{self.level}]score: {self.score}  height: {self.height}  speed: {self.height_speed} c_v: {self.connect_value}")

    def multi_move(self, steps):
        for s in steps:
            self.move(s[0], s[1])
        # self.print_board()

    def _connect_value(self):
        value = 0
        m = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 61: 0}
        count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 61: 0}
        merge_count = {0: 5, 1: 2, 2: 5, 3: 2, 4: 5, 61: 2}
        for i in self.board:
            if len(i) > 0:
                t = i[0]
                j = 1
                while j < len(i):
                    if i[j] != t:
                        break
                    j += 1
                count[t] += j

        for i in self.board:
            if len(i) > 1:
                t = i[0]
                j = 1
                while j < len(i):
                    if i[j] != t:
                        break
                    j += 1
                if j > 1 and count[t] < merge_count[t]:
                    value += m[t] * (j ** 2)
        if self.max_length() > 5:
            return value / (1 + (self.max_length() / 10.0 + self.std_length() + 0.00001))
        else:
            return value


class BoardOnline(Board):

    def move(self, a, b):
        """
        from a to b
        """
        req = requests.request('get',
                               url=f"{base_url}/move?token=wendachen&level={self.level}&from={a}&to={b}")
        res = req.json()
        try:
            self.board = res['board']
            self.score = res['score']
            if res['height'] - self.height > 0:
                self.height_speed = res['height'] - self.height
            self.height = res['height']
        except KeyError:
            logging.error(res)
            raise AssertionError
        self.connect_value = self._connect_value()
        self.total_num = self._total_num()
        self.add_score = self.score - self.origin_score


class BoardOffline(Board):
    def move(self, a, b):
        pop_value = []
        while True:
            if not self.board[a]:
                break
            if not pop_value:
                pop_value.append(self.board[a].pop(0))
            elif self.board[a][0] == pop_value[0]:
                pop_value.append(self.board[a].pop(0))
            else:
                break
        self.board[b] = pop_value + self.board[b]
        t = self.board[b][0]  # 硬币id

        if t != 61:
            s = 0  # 加起来的币值
            t = self.board[b][0]  # 硬币id
            c = 0  # 记录相同的硬币id位置
            if len(self.board[b]) > 1:
                for i in range(len(self.board[b])):
                    if self.board[b][i] == t:
                        c = i
                        s += {0: 0.01, 1: 0.05, 2: 0.1, 3: 0.5, 4: 1}[t]
                    else:
                        break
            if c > 0 and s in (0.05, 0.1, 0.5, 1, 5):
                self.score += s
                self.board[b] = self.board[b][c + 1:]
                if t <= 3:
                    self.board[b] = [t + 1] + self.board[b]
        else:
            # 魔法袋
            if len(self.board[b]) > 1:
                self.board[b] = self.board[b][1:]
                t = self.board[b][0]
                for i in range(5):
                    origin_len = len(self.board[i])
                    self.board[i] = [elem for elem in self.board[i] if elem != t]
                    new_len = len(self.board[i])
                    self.score += {0: 0.01, 1: 0.05, 2: 0.1, 3: 0.5, 4: 1}[t] * (
                            origin_len - new_len)
        self.connect_value = self._connect_value()
        self.total_num = self._total_num()
        self.add_score = self.score - self.origin_score

    def copy_to(self, board):
        board.board = self.board
        board.score = self.score
        board.height = self.height
        board.height_speed = self.height_speed
        board.origin_score = self.score


class BestMove:
    score = 0
    steps = []
    max_length = 10
    left_move = None
    count = 0
    move_times = 100
    connect_value = 0
    total_num = 100
    score_add = 0

    @classmethod
    def clear(cls):
        BestMove.score = 0
        BestMove.steps = []
        BestMove.max_length = 10
        BestMove.count = 0
        BestMove.move_times = 100
        BestMove.connect_value = -100
        BestMove.total_num = 100
        BestMove.score_add = 0


def evaluate_board(board: Board, k):
    """"""
    origin_score = board.score
    grade = 0
    grade += (1. / board.max_length()) * 50
    BestMove.clear()
    backtrack(board, k, [], 0)
    board.multi_move(BestMove.steps)
    add_score = board.score - origin_score
    grade += add_score

    # return 1./ board.max_length()
    return grade


def move_length(row):
    """移动的长度"""
    assert len(row) > 0
    t = row[0]
    i = 0
    for j in row:
        if j != t:
            break
        i += 1
    return i + 1


def backtrack(board: Board, move_left, steps: list, move_times):
    if move_left == 0:
        BestMove.count += 1
        # if board.max_length() < BestMove.max_length:
        return
    if board.max_length() <= 10:
        if board.add_score > 0:
            if BestMove.score_add == 0:
                BestMove.score_add = board.add_score
                BestMove.connect_value = -100
            if board.connect_value > BestMove.connect_value:
                BestMove.max_length = board.max_length()
                BestMove.steps = copy.deepcopy(steps)
                BestMove.score = board.score
                BestMove.move_times = move_times
                BestMove.connect_value = board.connect_value
        elif BestMove.score_add == 0:
            c_v = board.connect_value
            if c_v > BestMove.connect_value:
                BestMove.max_length = board.max_length()
                BestMove.steps = copy.deepcopy(steps)
                BestMove.score = board.score
                BestMove.move_times = move_times
                BestMove.connect_value = c_v
            elif c_v == BestMove.connect_value and move_times < BestMove.move_times:
                BestMove.max_length = board.max_length()
                BestMove.steps = copy.deepcopy(steps)
                BestMove.score = board.score
                BestMove.move_times = move_times
                BestMove.connect_value = c_v
            elif BestMove.max_length > board.max_length():
                BestMove.max_length = board.max_length()
                BestMove.steps = copy.deepcopy(steps)
                BestMove.score = board.score
                BestMove.move_times = move_times
                BestMove.connect_value = c_v
            elif move_times < BestMove.move_times:
                BestMove.max_length = board.max_length()
                BestMove.steps = copy.deepcopy(steps)
                BestMove.score = board.score
                BestMove.move_times = move_times
                BestMove.connect_value = c_v
    for i in range(5):
        for j in range(5):
            if i == j or \
                    len(board.board[i]) == 0 or \
                    (len(board.board[j]) + move_length(board.board[i]) + board.height + (
                            1 + move_times) * board.height_speed) >= 10:
                continue
            pre_board = copy.deepcopy(board.board)
            pre_score = board.score
            board.move(i, j)
            steps.append((i, j))
            move_left -= 1
            move_times += 1
            if board.max_length() < 10:
                backtrack(board, move_left, steps, move_times)
            steps.pop()
            move_times -= 1
            move_left += 1
            board.board = pre_board
            board.score = pre_score


if __name__ == '__main__':
    k = 4  # 穷举的步数
    test_result = {}
    for level in [1, 3, 5, 7]:
        try:
            print("level", level, "k", k)
            b = BoardOffline(level)
            b_online = BoardOnline(level)
            b_online.print_board()

            while True:
                # b_online.multi_move(BestMove.steps)
                next_move = None
                next_moves = None

                # best_grade = 0
                # for i in range(5):
                #     for j in range(5):
                #         if i == j:
                #             continue
                #         try_board = BoardOffline(0)
                #         b.copy_to(try_board)
                #         try:
                #             try_board.move(i, j)
                #         except IndexError:
                #             continue
                #         g = evaluate_board(try_board, k)
                #         if g > best_grade:
                #             best_grade = g
                #             next_move = (i, j)
                #             next_moves = copy.deepcopy([(i, j)] + BestMove.steps)

                try_board = BoardOffline(0)
                b.copy_to(try_board)
                BestMove.clear()
                backtrack(try_board, k, [], 0)
                next_moves = copy.deepcopy(BestMove.steps)

                if not next_moves:
                    # 当为空时 则将最长的挪至最短的
                    aaa = None
                    len_a = 0
                    bbb = None
                    len_b = 100
                    for ii, i in enumerate(try_board.board):
                        if len(i) > len_a:
                            len_a = len(i)
                            aaa = ii
                        if len(i) < len_b:
                            len_b = len(i)
                            bbb = ii
                    while aaa == bbb:
                        aaa = random.randint(0, 4)
                    next_moves = [(aaa, bbb)]

                print("move", next_moves)
                try:
                    b_online.multi_move(next_moves)
                except IndexError:
                    continue
                b.board = b_online.board
                b.score = b_online.score

                b_online.print_board()
        except AssertionError:
            test_result[level] = b_online.score
            continue
    print(test_result)
    print("avg", sum(test_result.values()) / len(test_result))
