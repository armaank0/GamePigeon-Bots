import json
from pynput.mouse import Button, Controller
import time

mouse = Controller()

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

# speed of mouse movments and delays
dur = 0.015 # faster than this value caused WordHunt to not register some inputs (during my testing)

# smooth mouse movement to simulate moving the mouse
def smooth_move(x, y, duration=dur):  
    start_x, start_y = mouse.position
    steps = 100
    delay = duration / steps

    for i in range(steps):
        t = i / steps
        x_pos = int(start_x + x*t)
        y_pos = int(start_y + y*t)
        mouse.position = (x_pos, y_pos)
        time.sleep(delay)
    mouse.position = (start_x + x, start_y + y)
    time.sleep(delay)

dist = 65.5 # mouse movement distance between cells; can be changed depending on the screen/cell size
current = 0
if __name__ == "__main__":
    while True:
        command = input("Enter the 4 rows of letters with the format 'abcd efgh ijkl mnop': ")
        if len(command) == 19:
            start_time = time.time()
            mouse.position = (88.5, 444.5) # initial mouse position; can be changed depending on where the game is located
            time.sleep(0.1)
            mouse.click(Button.left, 1) # click to highlight the mirroring window
            map = "".join(command.split())
            board1 = WordHunt(list(map))

            words = 0
            curr = 0
            for word in board1.sorted:
                index = 0
                if time.time() - start_time > 80: # in case there are too many words this will terminate the program at max time
                    print("Time limit exceeded!")
                    break
                for letter in board1.answers[word]:
                    x = (letter % 4) - (curr % 4)
                    y = (letter // 4) - (curr // 4)
                    if abs(x) >= 2 or y == 0:
                        for i in range(abs(x)):
                            smooth_move(x/abs(x)*dist, 0)
                            time.sleep(dur)
                        if abs(y) == 1:
                            smooth_move(0, y/abs(y)*dist)
                            time.sleep(dur)
                    if abs(y) >= 2 or x == 0:
                        for i in range(abs(y)):
                            smooth_move(0, y/abs(y)*dist)
                            time.sleep(dur)
                        if abs(x) == 1:
                            smooth_move(x/abs(x)*65.5, 0)
                            time.sleep(dur)
                    if abs(x) == 1 and abs(y) == 1:
                        smooth_move(x/abs(x)*dist, y/abs(y)*dist)
                        time.sleep(dur)
                    if index == 0:
                        mouse.press(Button.left)
                        time.sleep(dur)
                    index += 1
                    curr = letter
                mouse.release(Button.left)
                time.sleep(0.03)
                print(f"Completed word: {word} #{words}") # this line isn't necessary
                words += 1
                
            print(f"Completed! Total words: {words}") # some words are not recognized by the game, so not 100% accurate
            break
