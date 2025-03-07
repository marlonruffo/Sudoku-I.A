import json
import os
from datetime import datetime

def is_complete(board):
    """Verifica se o tabuleiro está completo."""
    for row in board:
        if 0 in row:
            return False
    return True


def save_board_to_json(board):

    jogos_folder = "jogos"

    if not os.path.exists(jogos_folder):
        os.makedirs(jogos_folder)

    existing_files = os.listdir(jogos_folder)
    sudoku_files = [f for f in existing_files if f.startswith("sudoku") and f.endswith(".json")]

    next_id = len(sudoku_files) + 1
    filename = f"sudoku_{next_id}.json"
    file_path = os.path.join(jogos_folder, filename)

    try:
        with open(file_path, "w") as file:
            json.dump(board, file, indent=4)
        print(f"Tabuleiro salvo em {file_path}")
    except Exception as e:
        print(f"Erro ao salvar o tabuleiro completo: {e}")
    


def log_move(board, attempted_move_quantity, row, col, value, valid_move, log_filename):
    """Salva o movimento no arquivo de log com detalhes de cada jogada."""
    move_data = {
        "attempted_move_quantity" : attempted_move_quantity,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "row": row,
        "col": col,
        "value": value,
        "valid_move": valid_move,
        "board_after_move": board
    }
    

    try:
        with open(log_filename, "r") as log_file:
            log_data = json.load(log_file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_data = []  

    log_data.append(move_data)
    
    try:
        with open(log_filename, "w") as log_file:
            json.dump(log_data, log_file, indent=4)  
    except Exception as e:
        print(f"Erro ao salvar no log: {e}")
