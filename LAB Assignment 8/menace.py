
from collections import Counter
import random


class Board:
    def __init__(self):
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

    def __str__(self):
        return   ( "\n 0 | 1 | 2     %s | %s | %s\n"
                   "---+---+---   ---+---+---\n"
                   " 3 | 4 | 5     %s | %s | %s\n"
                   "---+---+---   ---+---+---\n"
                   " 6 | 7 | 8     %s | %s | %s" % (self.board[0], self.board[1], self.board[2],
                                                self.board[3], self.board[4], self.board[5],
                                                self.board[6], self.board[7], self.board[8]))

    def is_possible(self, move):
        # If the move is in the range of 0 to 9 and the cell is empty in board
        if 0 <= move < 9 and self.board[move] == ' ':
            return True
        return False

    def is_winnig(self):

        for i in range(0,3):
            if self.board[i] != ' ' and self.board[0] == self.board[1] == self.board[2]:
                return True
            if self.board[i] != ' ' and self.board[i+3*i] == self.board[i+6*i]:
                return True

        if self.board[0] != ' ' and self.board[0] == self.board[4] == self.board[8]:
            return True

        if self.board[2] != ' ' and self.board[2] == self.board[4] == self.board[6]:
            return True

    def draw(self):
        for i in range(9):
            if self.board[i] != ' ':
                return False 
        return True

    def make_move(self, position, move):
        self.board[position] = move # '0 or X'

    def board_string(self):
        return ''.join(self.board)


class MenaceComputer:
    def __init__(self):
        self.matchboxes = {}
        self.num_win = 0
        self.num_draw = 0
        self.num_lose = 0

    def start_game(self):
        # To trackback the moves
        self.moves_played = []

    def get_move(self, board):
        # Find board in matchboxes and choose a bead
        # If the matchbox is empty, return -1 (resign)
        board = board.board_string()
        if board not in self.matchboxes:
            new_beads = [pos for pos, mark in enumerate(board) if mark == ' ']
            # Early boards start with more beads
            self.matchboxes[board] = new_beads * ((len(new_beads) + 2) // 2)

        beads = self.matchboxes[board]
        if len(beads):
            bead = random.choice(beads)
            self.moves_played.append((board, bead))
        else:
            bead = -1
        return bead

    def win_game(self):
        # We won, add three beads
        for (board, bead) in self.moves_played:
            self.matchboxes[board].extend([bead, bead, bead])
        self.num_win += 1

    def draw_game(self):
        # A draw, add one bead
        for (board, bead) in self.moves_played:
            self.matchboxes[board].append(bead)
        self.num_draw += 1

    def lose_game(self):
        # Lose, remove a bead
        for (board, bead) in self.moves_played:
            matchbox = self.matchboxes[board]
            del matchbox[matchbox.index(bead)]
        self.num_lose += 1

    def print_stats(self):
        print('Have learnt %d boards' % len(self.matchboxes))
        print('W/D/L: %d/%d/%d' % (self.num_win, self.num_draw, self.num_lose))

    def print_probability(self, board):
        board = board.board_string()
        print("Stats for this board: " + str(Counter(self.matchboxes[board]).most_common()))
        

class Human:
    def __init__(self):
        pass

    def start_game(self):
        print("Here We Go!!!")

    def get_move(self, board):
        while True:
            move = input('Make a move: ')
            if board.is_possible(move):
                break
            print("Not a valid move")
        return int(move)

    def win_game(self):
        print("Congrats.....You won!")

    def draw_game(self):
        print("Uff! Tough Game It's a draw.")

    def lose_game(self):
        print("You losssse. Better Luck Next Time!!")

def play_game(first, second, silent=False):
    first.start_game()
    second.start_game()
    board = Board()

    if not silent:
        print("\n\nStarting a new game!")
        print(board)

    while True:
        if not silent:
            first.print_probability()
        move = first.get_move(board)
        if move == -1:
            if not silent:
                print("Player has resigned his Game!!!")
            first.lose_game()
            second.win_game()
            break
        board.make_move(move, 'X')
        if not silent:
            print(board)
        if board.is_winning():
            first.win_game()
            second.lose_game()
            break
        if board.draw():
            first.draw_game()
            second.draw_game()
            break

        if not silent:
            second.print_probability(board)
        move = second.get_move(board)
        if move == -1:
            if not silent:
                print("Player has resigned his Game!!!")
            second.lose_game()
            first.win_game()
            break
        board.make_move(move, 'O')
        if not silent:
            print(board)
        if board.is_winning():
            second.win_game()
            first.lose_game()
            break


def main():
    go_first_menace = MenaceComputer()
    go_second_menace = MenaceComputer()
    human = Human()

    for i in range(1000):
        play_game(go_first_menace, go_second_menace, silent=True)

    go_first_menace.print_stats()
    go_second_menace.print_stats()

    play_game(go_first_menace, human)
    play_game(human, go_second_menace)


if __name__ == '__main__':
    main()