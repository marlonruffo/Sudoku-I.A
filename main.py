from sudoku import Sudoku
from utils import is_complete

def main():
    print("Bem-vindo ao Sudoku!")
    game = Sudoku()

    game_running = True
    while game_running:
        game.display_board()
        if is_complete(game.board):
            print("Parabéns! Você completou o Sudoku!")
            game_running = False
            continue

        print("\nDigite sua jogada no formato: linha coluna número (0 para sair)")
        try:
            user_input = input("Sua jogada: ")
            if user_input == "0":
                print("Obrigado por jogar!")
                game_running = False  
            else:

                # Colocar aqui os inputs
                row, col, num = map(int, user_input.split())
                game.make_move_from_input(row, col, num)  # Usando os valores inseridos pelo usuário
        except ValueError:
            print("Entrada inválida. Por favor, use o formato correto: linha coluna número")

if __name__ == "__main__":
    main()
