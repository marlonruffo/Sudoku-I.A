import random
import uuid
import os
import json
from utils import is_complete, log_move
from datetime import datetime


class Sudoku:
    def __init__(self): 
        self.logs_folder = "logs"
        if not os.path.exists(self.logs_folder):
            os.makedirs(self.logs_folder)
        self.sudoku_id = str(uuid.uuid4())  # ID único
        self.log_filename = os.path.join(self.logs_folder, f"sudoku_log_{self.sudoku_id}.json")
        self.board = [[0 for _ in range(9)] for _ in range(9)]  
        self.initialBoard = self.generate_random_board()
        self.attempted_moves = 0  
        self.valid_moves = 0     
        self.invalid_moves = 0   
        self.save_initial_log()
        print("O tabuleiro foi iniciado com: " + str(self.count_filled_cells()) + " valores")

    def generate_random_board(self):
        num_initial_cells = random.randint(17, 30)  
        """
        17 - 20 : Dificuldade Alta
        21 - 25 : Dificuldade Média
        26 - 30 : Dificuldade Fácil
        """
        print("Expectativa de iniciativa de tabuleiro: " + str(num_initial_cells))

        # Medida de segurança para evitar loop infinito
        attempts = 0  
        max_attempts = 1000  
        while attempts < max_attempts and num_initial_cells > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)

            if self.board[row][col] == 0:
                value = random.randint(1, 9)

                if self.is_valid_move(row, col, value):
                    self.board[row][col] = value
                    num_initial_cells -= 1  

            attempts += 1  
        return self.board
    def count_filled_cells(self):
        filled_cells = 0
        for row in self.board:
            filled_cells += sum(1 for cell in row if cell != 0)
        return filled_cells

    def display_board(self):
        for i, row in enumerate(self.board):
            if i % 3 == 0 and i != 0:
                print("-" * 21)

            for j, num in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(num if num != 0 else ".", end=" ")
            print()

    def is_valid_move(self, row, col, value):

        if value in self.board[row]:
            return False

        for r in range(9):
            if self.board[r][col] == value:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if self.board[r][c] == value:
                    return False
        return True

    def make_move(self, row, col, value):
        is_a_valid_move = False
        self.attempted_moves += 1  

        if self.board[row][col] == 0 and self.is_valid_move(row, col, value):
            self.board[row][col] = value
            is_a_valid_move = True
            self.valid_moves += 1  
        else:
            self.invalid_moves += 1  

        
        log_move(self.board, self.attempted_moves, row + 1, col + 1, value, is_a_valid_move, self.log_filename)
        return is_a_valid_move

    def make_move_from_input(self, row, col, num):
        if self.make_move(row - 1, col - 1, num):
            print("\nJogada realizada com sucesso!\n")
        else:
            print("\nJogada inválida. Tente novamente.\n")

    def display_move_counts(self):
        print(f"Tentativas de movimento: {self.attempted_moves}")
        print(f"Movimentos válidos: {self.valid_moves}")
        print(f"Movimentos inválidos: {self.invalid_moves}")

    def save_initial_log(self):
            """Salva o ID e o board inicial no arquivo de log"""
            initial_data = {
                "sudoku_id": self.sudoku_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "initial_board": self.initialBoard
            }
        
            if not os.path.exists(self.log_filename):
                try:
                    with open(self.log_filename, "w") as log_file:
                        json.dump([initial_data], log_file, indent=4)  
                except Exception as e:
                    print(f"Erro ao salvar o log inicial: {e}")

    def solve_sudoku_backtracking(self):
        return self._solve_sudoku_backtracking_helper()

    def _find_empty_location(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return row, col
        return None

    def _solve_sudoku_backtracking_helper(self):
        empty_location = self._find_empty_location()
        if not empty_location:
            return True  # Não há posições vazias, o Sudoku está resolvido

        row, col = empty_location

        for number in range(1, 10):
            if self.is_valid_move(row, col, number):
                self.board[row][col] = number

                if self._solve_sudoku_backtracking_helper():
                    return True

                # Desfaz a jogada (backtrack)
                self.board[row][col] = 0

        return False