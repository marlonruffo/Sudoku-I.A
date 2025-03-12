from sudoku import Sudoku
from utils import is_complete, save_board_to_json

def main():
    print("Bem-vindo ao Sudoku!")

    while True:
        print("\nSelecione uma opção:")
        print("1. Jogar Manualmente")
        print("2. Resolver por Busca por Backtracking")
        print("3. Resolver por Busca em Largura")
        print("4. Resolver por Busca em Profundidade")
        print("5. Resolver por Busca Ordenada")
        print("6. Resolver por Busca Gulosa")
        print("7. Resolver por A*")
        print("0. Sair")

        choice = input("Sua escolha: ")

        game = Sudoku()

        if choice == "1":
            print("Tabuleiro inicial:")
            game.display_board()
            
            game_running = True
            while game_running:
                game.display_board()
                if is_complete(game.board):
                    print("Parabéns! Você completou o Sudoku!")
                    game_running = False
                    break

                print("\nDigite sua jogada no formato: linha coluna número (0 para sair)")
                try:
                    user_input = input("Sua jogada: ")
                    if user_input == "0":
                        print("Obrigado por jogar!")
                        game_running = False
                        break
                    else:
                        row, col, num = map(int, user_input.split())
                        game.make_move_from_input(row, col, num)
                except ValueError:
                    print("Entrada inválida. Por favor, use o formato: linha coluna número")
        
        elif choice == "2":
            print("Tabuleiro inicial:")
            game.display_board()

            if game.solve_sudoku_backtracking():
                print("\nSudoku resolvido com sucesso!")
                steps = game.get_steps()
                print(f"Passos necessários para resolver: {steps}")

                print("\nTabuleiro resolvido:")
                game.display_board()
                
                #save_board_to_json(game.board)
            else:
                print("\nNão foi possível resolver o Sudoku.")
                steps = game.get_steps()
                print(f"Passos aplicados: {steps}")

        # elif choice == '3':

        elif choice == '4':
            print("Tabuleiro inicial:")
            game.display_board()

            if game.solve_sudoku_dfs():
                print("\nSudoku resolvido com sucesso!")
                steps = game.get_steps()
                print(f"Passos necessários para resolver: {steps}")

                print("\nTabuleiro resolvido:")
                game.display_board()
            else:
                print("\nNão foi possível resolver o Sudoku.")
                steps = game.get_steps()
                print(f"Passos aplicados: {steps}")        


        # elif choice == '5':

        # elif choice == '6':

        elif choice == '7':
            print("Tabuleiro inicial:")
            game.display_board()

            if game.solve_A_star():
                print("\nSudoku resolvido com sucesso!")
                steps = game.get_steps()
                print(f"Passos necessários para resolver: {steps}")

                print("\nTabuleiro resolvido:")
                game.display_board()
            else:

                print("\nNão foi possível resolver o Sudoku.")
                steps = game.get_steps()
                print(f"Passos aplicados: {steps}")   


        elif choice == "0":
            print("Saindo. Obrigado por usar o Sudoku Solver!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
