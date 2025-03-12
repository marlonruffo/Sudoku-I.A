import random
import uuid
import os
import json
from utils import is_complete, log_move, save_board_to_json
from datetime import datetime
import heapq
import copy
from copy import deepcopy

class Sudoku:

    def __init__(self, game): 
        self.logs_folder = "logs"
        self.bfs_folder = "busca_em_largura" 
        if not os.path.exists(self.logs_folder):
            os.makedirs(self.logs_folder)
        self.sudoku_id = str(uuid.uuid4())  # ID único
        self.log_filename = os.path.join(self.logs_folder, f"sudoku_log_{self.sudoku_id}.json")
        self.board = [[0 for _ in range(9)] for _ in range(9)]  
        self.attempted_moves = 0  
        self.valid_moves = 0     
        self.invalid_moves = 0
        self.steps = 0
        self.game = game
        self.initialBoard = self.generate_board()
        self.board = [row[:] for row in self.initialBoard]
        self.save_initial_log()
        print("O tabuleiro foi iniciado com: " + str(self.count_filled_cells()) + " valores")

    def update_initial_board(self):
        self.board = [row[:] for row in self.initialBoard]

    def generate_board(self):
        jogos_folder = "jogos"

        if not os.path.exists(jogos_folder):
            raise FileNotFoundError(f"A pasta '{jogos_folder}' não existe.")

        sudoku_files = [f for f in os.listdir(jogos_folder) if f.startswith("sudoku") and f.endswith(".json")]

        if not sudoku_files:
            raise FileNotFoundError("Nenhum arquivo de tabuleiro completo encontrado na pasta 'jogos'.")

        if self.game == -1:
            complete_sudoku_file = random.choice(sudoku_files)
            complete_sudoku_path = os.path.join(jogos_folder, complete_sudoku_file)
        else:
            # Ajustando a construção do nome do arquivo para o formato correto
            complete_sudoku_file = f"sudoku_{self.game}.json"
            complete_sudoku_path = os.path.join(jogos_folder, complete_sudoku_file)

            # Verifica se o arquivo específico existe com o nome correto
            if complete_sudoku_file not in sudoku_files:
                raise FileNotFoundError(f"O arquivo '{complete_sudoku_file}' não existe na pasta 'jogos'.")

        with open(complete_sudoku_path, "r") as file:
            complete_board = json.load(file)

        num_cells_remain = random.choices(
            population=[random.randint(17, 20), random.randint(21, 25), random.randint(26, 30)],
            weights=[1, 2, 3],
            k=1
        )[0]

        print(f"\nGerando um tabuleiro com {num_cells_remain} células preenchidas.")
        print(f"Tabuleiro gerado a partir do arquivo: {complete_sudoku_file}")

        cells_removed = 0
        while cells_removed < 81 - num_cells_remain:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if complete_board[row][col] != 0:
                complete_board[row][col] = 0
                cells_removed += 1

        self.initialBoard = complete_board

        return self.initialBoard

    def solve_sudoku_bfs(self):
        self.steps = 0
        initial_state = deepcopy(self.board)
        if not os.path.exists(self.bfs_folder):
            os.makedirs(self.bfs_folder)
            print(f"Pasta '{self.bfs_folder}' criada.")
        
        tree_info = {
            "levels": [],  
            "total_nodes": 0,  
            "max_level": 0,  
            "solution_found": False,
            "total_steps": 0
        }

        states = [(initial_state, 0)]  # Lista de tuplas (estado, nível)

        while states:
            current_state, current_level = states.pop(0)  
            self.board = deepcopy(current_state)
            self.steps += 1

            # Log de progresso
            if self.steps % 1000 == 0:  
                print(f"Passos realizados: {self.steps}, Estados na fila: {len(states)}")

            empty_location = self._find_empty_location()
            if not empty_location:
                tree_info["solution_found"] = True
                self._save_tree_info(tree_info)
                return True  

            row, col = empty_location

            # Atualiza o nível máximo
            if current_level > tree_info["max_level"]:
                tree_info["max_level"] = current_level

            # Adiciona informações sobre o nível atual
            if len(tree_info["levels"]) <= current_level:
                tree_info["levels"].append({"level": current_level, "nodes": 0})  

            tree_info["levels"][current_level]["nodes"] += 1
            tree_info["total_nodes"] += 1
            tree_info["total_steps"] = self.steps
            for number in range(1, 10):
                if self.is_valid_move(row, col, number):
                    new_state = deepcopy(current_state)
                    new_state[row][col] = number

                    # Adiciona o novo estado à lista de estados
                    states.append((new_state, current_level + 1))

        tree_info["total_steps"] = self.steps
        self._save_tree_info(tree_info)
        return False  

    def _save_tree_info(self, tree_info):
        filename = os.path.join(self.bfs_folder, f"sudoku_tree_info_{self.sudoku_id}.json")
        try:
            with open(filename, "w") as file:
                json.dump(tree_info, file, indent=4)
            print(f"Informações da árvore salvas em {filename}")
        except Exception as e:
            print(f"Erro ao salvar as informações da árvore: {e}")

    def _format_board(self, board):
        """Formata o tabuleiro para exibição no nó."""
        return "\n".join([" ".join(str(cell) if cell != 0 else "." for cell in row) for row in board])
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
    
    def is_valid_move_on_board(self, board, row, col, value):
        if value in board[row]:
            return False
        if any(board[r][col] == value for r in range(9)):
            return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if board[r][c] == value:
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

    def get_steps(self):
        return self.steps

    def solve_sudoku_backtracking(self):
        self.steps = 0
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
            return True
        
        row, col = empty_location

        for number in range(1, 10):
            if self.is_valid_move(row, col, number):
                self.board[row][col] = number
                self.steps += 1

                if self._solve_sudoku_backtracking_helper():
                    return True

                self.board[row][col] = 0

        return False
    
    def solve_sudoku_dfs(self):
        stack = [((0, 0), [row[:] for row in self.board])]  # position stack and board copy
        self.steps = 0

        while stack:
            (row, col), current_board = stack.pop()

            while row < 9 and current_board[row][col] != 0:
                col += 1
                if col == 9:
                    col = 0
                    row += 1

            if row == 9:
                self.board = current_board
                return True

            for number in range(1, 10):
                if self.is_valid_move_on_board(current_board, row, col, number):
                    new_board = [r[:] for r in current_board]
                    new_board[row][col] = number

                    if col == 8:
                        stack.append(((row + 1, 0), new_board))
                    else:
                        stack.append(((row, col + 1), new_board))
                    self.steps += 1

        return False
    
    def is_valid(self, row, col, num):
         """Verifica se um número pode ser colocado em uma célula específica."""
         for i in range(9):
             if self.board[row][i] == num or self.board[i][col] == num:
                 return False
         
         start_row, start_col = 3 * (row // 3), 3 * (col // 3)
         for i in range(3):
             for j in range(3):
                 if self.board[start_row + i][start_col + j] == num:
                     return False
         return True
 
    def get_empty_cells(self):
         """Retorna uma lista de células vazias ordenadas pelo número de possibilidades."""
         empty_cells = []
         for row in range(9):
             for col in range(9):
                 if self.board[row][col] == 0:
                     possibilities = [num for num in range(1, 10) if self.is_valid( row, col, num)]
                     heapq.heappush(empty_cells, (len(possibilities), row, col, possibilities))
         return empty_cells
     
    def print_board(self):
         """Imprime o tabuleiro atual de forma organizada."""
         for row in self.board:
             print(" ".join(str(num) if num != 0 else '.' for num in row))
         print("\n" + "-"*25 + "\n")
 
    def solve_A_star(self):
         """Resolve o Sudoku usando o algoritmo A*."""
         priority_queue = [(0, self.board)]  # (custo, estado_atual)
         iterations = 0  # Contador de iterações
         max_iterations = 10000  # Limite de iterações
         self.steps = 0
         
         while priority_queue:
             iterations += 1
             if iterations > max_iterations:
                 print("Limite de iterações atingido! Pode haver um loop infinito.")
                 return False
             
             _, current_board = heapq.heappop(priority_queue)
             self.board = current_board  # Atualiza a referência do tabuleiro
             empty_cells = self.get_empty_cells()
             
             if not empty_cells:
                 return current_board  # Solução encontrada
             
             _, row, col, possibilities = heapq.heappop(empty_cells)
             
             for num in possibilities:
                 new_board = copy.deepcopy(current_board)
                 new_board[row][col] = num
                 heapq.heappush(priority_queue, (len(empty_cells), new_board))
                 
             # Debug: Mostrar o tabuleiro a cada 100 iterações
             if iterations % 100 == 0:
                 print(f"\nEstado do tabuleiro após {iterations} iterações:")
                 self.print_board()
             self.steps = iterations
         
         return False  # Nenhuma solução encontrada