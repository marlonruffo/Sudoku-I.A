import random
import uuid
import os
import heapq
import json
from utils import is_complete, log_move, save_board_to_json
from datetime import datetime


class Sudoku:
    def __init__(self): 
        self.logs_folder = "logs"
        if not os.path.exists(self.logs_folder):
            os.makedirs(self.logs_folder)
        self.sudoku_id = str(uuid.uuid4())  # ID único
        self.log_filename = os.path.join(self.logs_folder, f"sudoku_log_{self.sudoku_id}.json")
        self.board = [[0 for _ in range(9)] for _ in range(9)]  
        #self.initialBoard = self.generate_random_board()
        self.initialBoard = self.generate_board()
        self.attempted_moves = 0  
        self.valid_moves = 0     
        self.invalid_moves = 0
        self.steps = 0   
        self.save_initial_log()
        print("O tabuleiro foi iniciado com: " + str(self.count_filled_cells()) + " valores")

    def generate_board(self):
        jogos_folder = "jogos"

        if not os.path.exists(jogos_folder):
            raise FileNotFoundError(f"A pasta '{jogos_folder}' não existe.")

        sudoku_files = [f for f in os.listdir(jogos_folder) if f.startswith("sudoku") and f.endswith(".json")]

        if not sudoku_files:
            raise FileNotFoundError("Nenhum arquivo de tabuleiro completo encontrado na pasta 'jogos'.")

        complete_sudoku_file = random.choice(sudoku_files)
        complete_sudoku_path = os.path.join(jogos_folder, complete_sudoku_file)

        with open(complete_sudoku_path, "r") as file:
            complete_board = json.load(file)

        num_cells_remain = random.choices(
            population=[random.randint(17, 20), random.randint(21, 25), random.randint(26, 30)],
            weights=[1, 2, 3],
            k=1
        )[0]

        print(f"Gerando um tabuleiro com {num_cells_remain} células preenchidas.")
        print(f"\nGerando novo tabuleiro a partir do arquivo: {complete_sudoku_file}\n")

        cells_removed = 0
        while cells_removed < 81 - num_cells_remain:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if complete_board[row][col] != 0:
                complete_board[row][col] = 0
                cells_removed += 1

        self.board = complete_board

        return self.board

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
    
    def solve_sudoku_ordered(self, debug=False, debug_interval=1000, max_iterations=1000000):
        """
        Implementa a busca ordenada (custo uniforme) para resolver o Sudoku,
        onde o custo de preencher uma célula é definido como:
            custo = 1 + 0.1 * (linha + coluna)
        Durante a busca, guarda o estado com o maior número de células preenchidas.
        Se o limite de iterações for atingido, esse estado parcial é exibido.
        
        Parâmetros:
        - debug: se True, imprime mensagens de depuração.
        - debug_interval: intervalo de iterações para exibir status.
        - max_iterations: número máximo de iterações permitidas.
        """
        self.steps = 0
        open_list = []
        count = 0  # contador para desempate (mantém a ordem de inserção)
        initial_board = [row[:] for row in self.board]
        heapq.heappush(open_list, (0, count, initial_board))
        visited = set()
        iterations = 0

        # Variáveis para manter o melhor estado parcial
        best_state = None
        best_filled_count = -1

        while open_list:
            iterations += 1
            if debug and iterations % debug_interval == 0:
                print(f"Iteração {iterations}: open_list tamanho = {len(open_list)}, passos = {self.steps}, custo atual = {open_list[0][0]:.2f}")
            if iterations > max_iterations:
                print("Limite máximo de iterações atingido. Encerrando busca para depuração.")
                if best_state is not None:
                    self.board = best_state
                    print(f"Melhor estado parcial com {best_filled_count} células preenchidas:")
                    self.display_board()
                return False

            cost, _, current_board = heapq.heappop(open_list)

            # Atualiza o melhor estado parcial, se o atual tiver mais células preenchidas
            filled_count = sum(1 for row in current_board for cell in row if cell != 0)
            if filled_count > best_filled_count:
                best_filled_count = filled_count
                best_state = current_board

            if is_complete(current_board):
                self.board = current_board
                if debug:
                    print(f"Solução encontrada em {iterations} iterações com custo total {cost:.2f}.")
                return True

            # Encontra a primeira célula vazia (ordem fixa)
            empty_cell = None
            for row in range(9):
                for col in range(9):
                    if current_board[row][col] == 0:
                        empty_cell = (row, col)
                        break
                if empty_cell is not None:
                    break

            if empty_cell is None:
                continue

            # Define o custo adicional para preencher a célula, escalado para não aumentar demais
            additional_cost = 1 + 0.1 * (empty_cell[0] + empty_cell[1])

            # Expande o nó: tenta preencher a célula vazia com números de 1 a 9
            for num in range(1, 10):
                if self.is_valid_move_on_board(current_board, empty_cell[0], empty_cell[1], num):
                    new_board = [r[:] for r in current_board]
                    new_board[empty_cell[0]][empty_cell[1]] = num
                    new_cost = cost + additional_cost
                    board_tuple = tuple(tuple(r) for r in new_board)
                    if board_tuple in visited:
                        continue
                    visited.add(board_tuple)
                    count += 1
                    heapq.heappush(open_list, (new_cost, count, new_board))
                    self.steps += 1

        print("Busca encerrada sem encontrar solução.")
        return False




