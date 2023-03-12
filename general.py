import math
import os
from colorama import *

init() # colorama

class Board:
  def __init__(self, players, size):
    self.players = players
    self.winners = []
    self.width, self.height = size
    self.grid = [[' ' for i in range(self.width)] for j in range(self.height)]
    self.lowest = [self.height for i in range(self.width)]
    self.fullCols = []
    self.allMoves = []
  
  def __str__(self):
    N = len(str(self.width))
    numList = [f'{n:0{N}d}' for n in range(self.width)]
    digList = [[n[i] for n in numList] for i in range(N)]
    numbering = Fore.CYAN + '\n'.join(['|' + '|'.join(i) + '|' for i in digList]) + Fore.WHITE

    output = '--- ALL PLAYERS ---\n'
    for p in self.players:
      output += str(p) + '\n'

    output += '\n' + numbering + '\n'

    for i, row in enumerate(self.grid):
      output += '|' + '|'.join([Fore.GREEN+x+Fore.WHITE if x in self.winners else Fore.YELLOW+x+Fore.WHITE if ([None]+self.allMoves)[-1] == (i, j) else x for j, x in enumerate(row)]) + '|\n'
    
    output += numbering
    return output
  
  def isOver(self):
    return len(self.winners) == len(self.players) - 1
  
  def isDraw(self):
    return len(self.fullCols) == self.width

class Player:
  def __init__(self, name, symbol):
    self.name = name
    self.symbol = symbol
    self.hasWon = False
  
  def __str__(self):
    generic = f'{self.name}: {self.symbol}'
    return Fore.GREEN+f'{generic} (HAS WON)'+Fore.WHITE if self.hasWon else generic
  
  def check_winner(self, board:Board):
    # check horizontal spaces
    for y in range(board.height):
      for x in range(board.width - 3):
        if board.grid[x][y] == board.grid[x+1][y] == board.grid[x+2][y] == board.grid[x+3][y] == self.symbol:
          return True

    # check vertical spaces
    for x in range(board.width):
      for y in range(board.height - 3):
        if board.grid[x][y] == board.grid[x][y+1] == board.grid[x][y+2] == board.grid[x][y+3] == self.symbol:
          return True

    # check / diagonal spaces
    for x in range(board.width - 3):
      for y in range(3, board.height):
        if board.grid[x][y] == board.grid[x+1][y-1] == board.grid[x+2][y-2] == board.grid[x+3][y-3] == self.symbol:
          return True

    # check \ diagonal spaces
    for x in range(board.width - 3):
      for y in range(board.height - 3):
        if board.grid[x][y] == board.grid[x+1][y+1] == board.grid[x+2][y+2] == board.grid[x+3][y+3] == self.symbol:
          return True
    return False  
  
  def move(self, board:Board, col):
    board.grid[board.lowest[col]-1][col] = self.symbol
    board.lowest[col] -= 1

    if board.lowest[col] == 0:
      board.fullCols.append(col)

    board.allMoves.append((board.lowest[col], col))
    
    if self.check_winner(board):
      board.winners.append(self.symbol)
      self.hasWon = True


def inputSettings():
  players = []
  names = []
  symbols = []

  # Adding players
  while True:
    inputPlayer = input('\nInput player name and symbol\nSYNTAX: "name symbol"\n(TYPE "END" TO FINISH) > ').strip(' ')
    if inputPlayer.upper() == 'END': 
      if len(players) >= 2: break
      else: 
        print('Needs at least 2 players, add more!')
        continue

    try:
      name, symbol = inputPlayer.split(' ')

      if len(symbol) != 1:
        print('Sorry, wrong syntax!')
        continue        

      names.append(name)
      symbols.append(symbol)
    except:
      print('Sorry, wrong syntax!')
      continue
  
    if name in names[:-1]: 
      print('Sorry, name already taken')
      continue
    if symbol in symbols[:-1]: 
      print('Sorry, symbol already taken!')
      continue

    players.append(Player(name, symbol))
    playerNo = len(players)

  # Making the board
  boardSize = (0, 0)
  minSize = (minLength := playerNo*2, minLength)
  defaultSize = (defLength := math.floor(1.5*(playerNo**2)), defLength)
  
  while True:
    boardSize = input('\nInput size of board\nSYNTAX: "width height"\n(TYPE "DEF" FOR DEFAULT SIZE AND "MIN" FOR MINIUMUM SIZE) > ').upper()
    if boardSize == 'MIN':
      width, height = minSize
      print(f'Minimum board size: ({minLength}, {minLength})')
      boardSize = minSize
      break
    if boardSize == 'DEF':
      width, height = defaultSize
      print(f'Default board size: ({defLength}, {defLength})')
      boardSize = defaultSize
      break
    
    try:
      width, height = [int(x) for x in boardSize.split(' ')]
      if width < minLength or height < minLength:
        print(f'Sorry, width and length must be at least {minLength}!')  
      else: 
        boardSize = (int(width), int(height))
        break    
    except:
      print('Sorry, wrong syntax!')

  # Verify data
  print('\n--- PLAYER NAMES & SYMBOLS ---\n(player: symbol)')
  print('\n'.join([str(p) for p in players]))
  print(f'\n--- BOARD SIZE: ---\nwidth {width}, height {height}')

  isOk = input('\nIs the above correct?\n(TYPE "YES" FOR YES, OTHERWISE NO) > ').upper() == 'YES'
  if not isOk: return inputSettings()
  return players, boardSize, symbols


def main():
  os.system('title CONNECT 4')

  players, boardSize, symbols = inputSettings()
  os.system('cls')

  board = Board(players, boardSize)
  print(board)
  
  pIndex = 0
  while not (board.isOver() or board.isDraw()):
    p = players[pIndex]
    if p.symbol in board.winners: 
      pIndex += 1
      if pIndex == len(players): pIndex = 0
      continue

    col = input(f'\n{p.name}\'s turn, pick a column > ')
    print()

    try:
      colI = int(col)

      if colI < 0 or colI >= board.width:
        print(f'Sorry, you must pick a column between 0 and {board.width-1}!')
        continue    

      if colI in board.fullCols:
        print(f'Sorry, column {colI} is not available!') 
        continue

      p.move(board, colI)
      pIndex += 1
      if pIndex == len(players): pIndex = 0

      os.system('cls')
      print(board)
    except:
      print('Sorry, wrong syntax!')
  
  print('\n--- GAME RESULTS ---')

  # PRINTING WINNERS (IF ANY)
  if board.winners != []:
    print('WINNERS (IN ORDER):')
    for p in (wins:=[players[symbols.index(p)] for p in board.winners]): print(f'  {p}')

  if board.isDraw(): print('DRAWN:') # PRINTING DRAWNS (IF ANY)
  else: print('LEFTOVER:')           # PRINTING LEFTOVER PLAYERS OTHERWISE

  print('\n'.join(['  '+str(p) for p in board.players if p not in wins]))

  input('\nEnter to end the program > ')

if __name__ == "__main__":
  main()