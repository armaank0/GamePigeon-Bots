import json
import serial
import time

# Check that the port name matches
s = serial.Serial(port='/dev/cu.usbmodemHIDGD1', baudrate=115200, timeout=0.1)

class WordHunt:
    def __init__(self, board: list):
        self.board = [letter.lower() for letter in board]
        self.answers = {}
        self.sorted = []
        self.word_list = {}

        self.verify_board()
        self.get_word_list()
        self.solve_board()
        self.sort_answers()

    def verify_board(self):
        if len(self.board) != 16:
            raise IndexError("Board must have exactly 16 letters!")
        for letter in self.board:
            if len(letter) != 1:
                raise ValueError("Letters in board must be a single character in length!")
            if not 97 <= ord(letter) <= 122:
                raise ValueError("Board must contain only letters!")

    def get_word_list(self):
        with open("wordlist.json") as file:
            self.word_list = json.load(file)

    def solve_board(self):
        for cell_index in range(len(self.board)):
            cell = self.board[cell_index]
            possible_words = self.word_list[cell]
            self.answers.update(self.solve_adjacent_cells(cell_index, [], possible_words))

    def sort_answers(self):
        self.sorted = sorted(list(self.answers.keys()), key=len, reverse=True)

    def solve_adjacent_cells(self, cell_index: int, previous_word_indexes: list, possible_words: list):
        results = {}

        # updates the current word to include the current cell
        current_word_indexes = previous_word_indexes.copy()
        current_word_indexes.append(cell_index)

        # look for matches and cull impossible words
        new_possible_words = []
        if len(current_word_indexes) >= 3:
            for word in possible_words:
                if word == self.index_to_word(current_word_indexes):
                    results[word] = current_word_indexes
                elif word.startswith(self.index_to_word(current_word_indexes)):
                    new_possible_words.append(word)
        else:
            new_possible_words = possible_words

        if len(new_possible_words) > 0:
            for adjacent_cell in self.get_adjacent_cells(cell_index, current_word_indexes):
                results.update(self.solve_adjacent_cells(adjacent_cell, current_word_indexes, new_possible_words))

        return results

    @staticmethod
    def get_adjacent_cells(cell_index: int, previous_cells: list):
        adjacent_positions = []

        # gets the relative position of all adjacent cells
        left = (cell_index % 4 != 0)
        right = (cell_index % 4 != 3)
        top = (cell_index >= 4)
        bottom = (cell_index < 12)

        if top and left:
            adjacent_positions.append(cell_index - 5)
        if top and right:
            adjacent_positions.append(cell_index - 3)
        if top:
            adjacent_positions.append(cell_index - 4)
        if left:
            adjacent_positions.append(cell_index - 1)
        if right:
            adjacent_positions.append(cell_index + 1)
        if bottom and left:
            adjacent_positions.append(cell_index + 3)
        if bottom:
            adjacent_positions.append(cell_index + 4)
        if bottom and right:
            adjacent_positions.append(cell_index + 5)

        # only includes cells not already used
        adjacent_cells = [cell for cell in adjacent_positions if cell not in previous_cells]

        return adjacent_cells

    # converts a list of indexes to an actual word
    def index_to_word(self, word_indexes: list):
        word = ""
        for letter_index in word_indexes:
            word += self.board[letter_index]
        return word


current = 0
if __name__ == "__main__":
    s.write(bytes('w,26/31\n', 'utf-8'))
    s.write(bytes('n\n', 'utf-8'))

    while True:
        command = input("Enter 'm' to re-position or the 4 rows of letters with the format 'abcd efgh ijkl mnop': ")
        if command == 'm':
            s.write(bytes('w,26/31\n', 'utf-8'))
            s.write(bytes('n\n', 'utf-8'))
        elif len(command) == 19:
            map = "".join(command.split())
            board1 = WordHunt(list(map))

            curr = 0
            br_moves = 0
            bl_moves = 0
            tr_moves = 0
            tl_moves = 0
            for word in board1.sorted:
                index = 0
                for letter in board1.answers[word]:
                    x = (letter % 4) - (curr % 4)
                    y = (letter // 4) - (curr // 4)
                    if abs(x) >= 2 or y == 0:
                        for i in range(abs(x)):
                            s.write(bytes('m,' + str((x/abs(x)) * 47) + '/' + '0' + '\n', 'utf-8'))
                            time.sleep(0.03)
                        if abs(y) == 1:
                            s.write(bytes('m,' + '0' + '/' + str(((y/abs(y)) * 47)) + '\n', 'utf-8'))
                            time.sleep(0.03)
                    if abs(y) >= 2 or x == 0:
                        for i in range(abs(y)):
                            s.write(bytes('m,' + '0' + '/' + str(((y/abs(y)) * 47)) + '\n', 'utf-8'))
                            time.sleep(0.03)
                        if abs(x) == 1:
                            s.write(bytes('m,' + str((x/abs(x)) * 47) + '/' + '0' + '\n', 'utf-8'))
                            time.sleep(0.03)
                    if abs(x) == 1 and abs(y) == 1:
                        s.write(bytes('m,' + str((x/abs(x)) * 42) + '/' + str(((y/abs(y)) * 42)) + '\n', 'utf-8'))
                        time.sleep(0.03)
                        if x/abs(x) == 1 and y/abs(y) == 1:
                            br_moves += 1
                        elif x/abs(x) == -1 and y/abs(y) == 1:
                            bl_moves += 1
                        elif x/abs(x) == 1 and y/abs(y) == -1:
                            tr_moves += 1
                        elif x/abs(x) == -1 and y/abs(y) == -1:
                            tl_moves += 1

                        if br_moves == 7:
                            s.write(bytes('m,8/8\n', 'utf-8'))
                            time.sleep(0.03)
                            br_moves = 0
                        elif bl_moves == 7:
                            s.write(bytes('m,-8/8\n', 'utf-8'))
                            time.sleep(0.03)
                            bl_moves = 0
                        elif tr_moves == 7:
                            s.write(bytes('m,8/-8\n', 'utf-8'))
                            time.sleep(0.03)
                            tr_moves = 0
                        elif tl_moves == 7:
                            s.write(bytes('m,-8/-8\n', 'utf-8'))
                            time.sleep(0.03)
                            tl_moves = 0
                    if index == 0:
                        s.write(bytes('l\n', 'utf-8'))
                        time.sleep(0.03)
                    index += 1
                    curr = letter
                s.write(bytes('n\n', 'utf-8'))
                time.sleep(0.03)
            print("Completed!")
            break
