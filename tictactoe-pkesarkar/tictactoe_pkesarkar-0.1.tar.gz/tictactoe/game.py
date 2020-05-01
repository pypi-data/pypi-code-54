import os
os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c') #for windows only. If you are using linux/Mac use os.system("clear")
class TicTacToe():
    def __init__(self):
        self.cells = ['_']*9
    def display(self):
        print(self.cells[0]+'|' + self.cells[1] + '|' + self.cells[2])
        print(self.cells[3]+'|' + self.cells[4] + '|' + self.cells[5])
        print(self.cells[6]+'|' + self.cells[7] + '|' + self.cells[8])
    def update_cell(self,cell_no,player):
        if self.cells[cell_no] == '_':
            self.cells[cell_no] = player
    def win_game(self,player):
        if (self.cells[0] == player and self.cells[1] == player and self.cells[2] == player):
            return True
        if (self.cells[3] == player and self.cells[4] == player and self.cells[5] == player):
                    return True
        if  (self.cells[6] == player and self.cells[7] == player and self.cells[8] == player):
                    return True
        if (self.cells[0]  == player and self.cells[4]  == player and self.cells[8] == player):
                    return True
        if (self.cells[6]  == player and self.cells[4]  == player and self.cells[2] == player):
                    return True
        if  (self.cells[0] == player and self.cells[3] == player and self.cells[6] == player):
                    return True
        if (self.cells[1]  == player and self.cells[4]  == player and self.cells[7] == player):
                    return True
        if (self.cells[2]  == player and self.cells[5]  == player and self.cells[8] == player):
                    return True
        return False

    def reset(self):
        self.cells = ['_']*9

board = TicTacToe()

def game_title():
    print("Lets Play Tic Tac Toe!")
    print("Instructions:")
    print("    First box on left up corner is 0")
    print("    Last box on  right down corner is 8")
    print("    Please pick the position of the number between 0 and 8")
    print("    if value below 0 or above 8 is entered, the player loses a turn!")
    print("    if a string value is entered instead of a number then the player loses a turn!")
    print("    Type exit if you want to leave the game")


def refresh_screen():
    os.system('cls' if os.name == 'nt' else 'echo -e \\\\033c')
    
    game_title()
    
    board.display()


x_lst = []
o_lst = []
while True:
    refresh_screen()
    
    def input_x(x):
        
        x=int(x)
        return x
    x=(input('Pick position between 0-8:  '))
    
    if x == 'exit':
        break
    else:

        if x in x_lst:
            input_x(x)
        else:
            try:
                x = int(x)

            except ValueError:
                print('Thats not a number')
            else:
                if 0 <= x < 9:
                    board.update_cell(x,'X')
                                       
                else:
                     input_x(x)
    
    refresh_screen()
    if board.win_game("X"):
        print("X is the winner!")
        play_again = input("Start new game? Y/N  ").upper()
        if play_again == 'Y':
            board.reset()
            continue
        else:
            break
    

    def input_o(o):
        o=int(o)
        return o
    o=(input('Pick position between 0-8:  '))
    if o == 'exit':
        break
    else:

        if o in o_lst:
            input_o(o)
        else:
            try:
                o = int(o)
            except ValueError:
                print('Thats not a number')
            else:
                if 0 <= o < 9:
                    board.update_cell(o,'O')
                    if board.win_game("O"):
                        print("O is the winner!")
                        play_again = input("Start new game? Y/N  ").upper()
                        if play_again == 'Y':
                            board.reset()
                            continue
                        else:
                            break
                else:
                     input_o(o)
    refresh_screen()
    
