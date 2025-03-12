from sudoku import Sudoku
from utils import is_complete, save_board_to_json

def menu():
    print("\nSelecione uma opção:")
    print("1. Resolver por Busca por Backtracking")
    print("2. Resolver por Busca em Largura")
    print("3. Resolver por Busca em Profundidade")
    print("4. Resolver por Busca Ordenada")
    print("5. Resolver por Busca Gulosa")
    print("6. Resolver por A*")
    print("7. Resolver por Todos os Métodos")
    print("0. Sair/Voltar")

def sucess(game):
    print("Sudoku resolvido com sucesso!")
    steps = game.get_steps()
    print(f"Passos necessários para resolver: {steps}")

def tabuleiro_resolvido(game):
    print("\nTabuleiro resolvido:")
    game.display_board()

def fail(game):
    print("\nNão foi possível resolver o Sudoku.")
    steps = game.get_steps()
    print(f"Passos aplicados: {steps}")  

def game_options(game, second_choice):
    if second_choice == "1":

        print("Tabuleiro inicial:")
        game.display_board()

        if game.solve_sudoku_backtracking():
            sucess(game)
            print("Resolvido por Backtracking")
            tabuleiro_resolvido(game)
            
        else:
            fail(game)

    elif second_choice == '2':
        print("Tabuleiro inicial:")
        game.display_board()

        if game.solve_sudoku_bfs():
            sucess(game)
            print("Resolvido por BFS")
            tabuleiro_resolvido(game)            
        else:
            fail(game)

    elif second_choice == '3':
        print("Tabuleiro inicial:")
        game.display_board()

        if game.solve_sudoku_dfs():
            sucess(game)
            print("Resolvido por DFS")
            tabuleiro_resolvido(game)

        else:
            fail(game)

    elif second_choice == '4':
        print("Tabuleiro inicial:")
        game.display_board()

        if game.solve_sudoku_ordered():
            sucess(game)
            print("Resolvido por Ordered")
            tabuleiro_resolvido(game)
        else:
            fail(game)

    # elif second_choice == '5':
    #     print("Tabuleiro inicial:")
    #     game.display_board()

    #     if game.gulosa_sudoku_solver():
    #         sucess(game)
    #         print("Resolvido por Gulosa")
    #         tabuleiro_resolvido(game)
    #     else:
    #         fail(game)

    elif second_choice == '6':
        print("Tabuleiro inicial:")
        game.display_board()
        if game.solve_A_star():
            sucess(game)
            print("Resolvido por A*")
            tabuleiro_resolvido(game)
        else:
            fail(game)

    elif second_choice == '7':

        print("Tabuleiro inicial:")
        game.display_board()
        print()

        # Backtracking
        if game.solve_sudoku_backtracking():
            
            sucess(game)
            print("Resolvido por Backtracking")
            tabuleiro_resolvido(game)
            game.update_initial_board()
        else:
            fail(game)
        # # BFS
        if game.solve_sudoku_bfs():
            sucess(game)
            print("Resolvido por BFS")
            tabuleiro_resolvido(game)
            game.update_initial_board
        else:
            fail(game)

        # DFS
        if game.solve_sudoku_dfs():
            sucess(game)
            print("Resolvido por DFS")
            tabuleiro_resolvido(game)
            game.update_initial_board()
        else:
            fail(game)
        # # Ordered
        # if game.solve_sudoku_ordered():
        #     sucess(game)
        #     print("Resolvido por Ordered")
        #     tabuleiro_resolvido(game)
        #     game.update_initial_board()
        # else:
        #     fail(game)
        # # Gulosa
        # if game.gulosa_sudoku_solver():
        #     sucess(game)
        #     print("Resolvido por Gulosa")
        #     tabuleiro_resolvido(game)
        #     game.update_initial_board()
        # else:
        #     fail(game)
        # # A*
        if game.solve_A_star():
            sucess(game)
            print("Resolvido por A*")
            tabuleiro_resolvido(game)
            game.update_initial_board
        else:
            fail(game)


def main():
    print("Bem-vindo ao Sudoku!")
    fixed_board = None  # Variável para armazenar o tabuleiro fixo
    selected_game = None  # Armazena o número do jogo escolhido

    while True:
        print("\nSelecione uma opção:")
        print("1. Jogar Jogo Aleatório")
        print("2. Jogar Jogo Existente")
        print("0. Sair")

        first_choice = input("Sua escolha: ")

        if first_choice == "1":
            while True:
                game = Sudoku(-1)
                fixed_board = [row[:] for row in game.initialBoard]  # Salva o tabuleiro fixo

                menu()
                second_choice = input("Sua escolha: ")

                if second_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                    game_options(Sudoku(-1, fixed_board), second_choice)      

                elif second_choice == "0":
                    print("Saindo. Obrigado por usar o Sudoku Solver!")
                    break
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")                    

        elif first_choice == "2":
            while True:
                try:
                    game_choice = input("Escolha um jogo entre 1 a 200: ")
                    game_choice_int = int(game_choice)

                    if 1 <= game_choice_int <= 200:
                        break
                    else:
                        print("O valor deve estar entre 1 e 200. Tente novamente.")

                except ValueError:
                    print("Entrada inválida! Por favor, insira um número entre 1 e 200.")

            selected_game = game_choice_int  # Salva o número do jogo escolhido
            
            # Gerar o tabuleiro uma única vez e armazená-lo
            game = Sudoku(selected_game)
            fixed_board = [row[:] for row in game.initialBoard]

            while True:
                menu()
                second_choice = input("Sua escolha: ")

                if second_choice in ["1", "2", "3", "4", "5", "6", "7"]:
                    game_options(Sudoku(selected_game, fixed_board), second_choice)

                elif second_choice == "0":
                    print("Voltando para a tela inicial!")
                    break
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")      

        elif first_choice == "0":
            print("Saindo. Obrigado por usar o Sudoku Solver!")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")



if __name__ == "__main__":
    main()