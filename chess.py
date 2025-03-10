import random

white = ['P','R','N','B','Q','K']
black = ['p','r','n','b','q','k']

star = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,-1),(0,1)]
diag = [(1,1),(-1,-1),(1,-1),(-1,1)]
straight = [(1,0),(0,1),(-1,0),(0,-1)]
L = [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)]
wp = [(1,1),(-1,1)]
bp = [(-1,-1),(1,-1)]


    
class piece:
    def __init__ (self, pointer_to_board , file, rank, piece_notation):
        #board
        self.board = pointer_to_board
        
        #type
        self.notation = piece_notation
        
        #team
        self.color = 'white' if piece_notation in ['P','R','N','B','Q','K'] else 'black'
        
        #location on board
        self.file = file
        self.rank = rank
        
        
<<<<<<< HEAD
=======

        
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
        #movement style
        if self.notation in ['P','N','K','p','n','k']:
            self.distance = 1
        else:
            self.distance = 8
            
        #attack pattern
        if self.notation in ['Q','K','q','k']:
            self.attack_pattern = star
        
        elif self.notation in ['R','r']:
            self.attack_pattern = straight
            
        elif self.notation in ['B','b']:
            self.attack_pattern = diag
        
        elif self.notation in ['N','n']:
            self.attack_pattern = L
            
        elif self.notation in ['P']:
            self.attack_pattern = wp
        
        elif self.notation in ['p']:
            self.attack_pattern = bp
<<<<<<< HEAD
            
            
        
        #pawn parameters
=======
        print (self.notation)
        print (self.attack_pattern)
            
        #pawn parameters
        self.has_moved = False
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
        self.en_passant_rights = False
            
        #string representation
    def __str__ (self):
        return self.notation
    
    #returns squares the piece is currently attacking
<<<<<<< HEAD
    def target_squares (self,board): 
=======
    def target_squares (self): 
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
        targets = []
        for delta_file, delta_rank in self.attack_pattern:
            for dist in range(self.distance):
                target_file = self.file + ((dist+1)*delta_file)
                target_rank = self.rank + ((dist+1)*delta_rank)
                if 8 > target_rank >= 0 and 8 > target_file >= 0:
<<<<<<< HEAD
                    target = str(board[target_file][target_rank])
=======
                    target = str(self.board[target_file][target_rank])
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
                    if target != '_':
                        if self.notation in white and target in black:
                            targets.append((target_file,target_rank))
                        if self.notation in black and target in white:
                            targets.append((target_file,target_rank))
                        break
                    else:
                        pass
                        targets.append((target_file,target_rank))
                else:
                    break
<<<<<<< HEAD

        if self.notation == 'Q':
            print ('targs',targets)
        return targets
    
    def move (self):
        pass
        

class game:
    def __init__ (self):
        self.board = [
        ['B', 'K', '_', '_', 'P', 'p', '_', '_'],
        ['Q', '_', 'q', 'r', '_', '_', '_', '_'],
        ['_', '_', '_', 'k', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', 'P', 'p', '_', '_', '_', 'b'],
        ['_', '_', '_', 'N', 'B', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', 'P', '_', 'p', '_', '_']
        ]
        self.board2 = [
        ['R', 'P', '_', '_', '_', '_', 'p', 'r'],
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'],
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'],
        ['Q', 'P', '_', '_', '_', '_', 'p', 'q'],
        ['K', 'P', '_', '_', '_', '_', 'p', 'k'],
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'],
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'],
        ['R', 'P', '_', '_', '_', '_', 'p', 'r']
        ]
        self.populate(self.board)
        
        self.rook_a_has_moved = {
            'white':False,
            'black':False
            }
        
        self.rook_h_has_moved = {
            'white':False,
            'black':False
            }
        
        self.king_has_moved = {
            'white':False,
            'black':False
            }

        self.turn = 'white'
        self.winner = None
    
    def populate (self,board):
        self.white = []
        self.black = []
        for file in range(len(board)):
            for rank in range(len(board[file])):
                notation = board[file][rank]
                if notation != '_':
                    if not isinstance(board[file][rank], piece):
                        new_piece = piece(board, file, rank, notation)
                        board[file][rank] = new_piece
                    if str(notation) in {'P','R','N','B','Q','K'}:
                        self.white.append(board[file][rank])
                    else:
                        self.black.append(board[file][rank])
        self.board = board

        
    def in_check(self, color, board):
        attacked_squares = []
        attackers = self.black if color == "white" else self.white
        king_notation = "K" if color == "white" else "k"

        for piece in attackers:
            attacked_squares += piece.target_squares(board)
            if any(str(board[file][rank]) == king_notation for file, rank in attacked_squares):
                print (piece.notation)

        return any(str(board[file][rank]) == king_notation for file, rank in attacked_squares)
    
    def promotion (self,board):
        promotion_boards = []
        for file in range(len(board)):
            if board[file][0] == 'p':
=======
        return targets
    
    def move (self):
        pass
        

class game:
    def __init__ (self):
        self.board = [
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['_', '_', '_', '_', '_', '_', '_', '_'],
        ['B', '_', '_', '_', '_', '_', '_', '_'],
        ['_', 'p', '_', '_', '_', '_', '_', '_']
        ]
        self.populate()
        
    
    def populate (self):
        self.white = []
        self.black = []
        for file in range(len(self.board)):
            for rank in range(len(self.board[file])):
                notation = self.board[file][rank]
                if notation != '_':
                    new_piece = piece(self.board, file, rank, notation)
                    self.board[file][rank] = new_piece
                    if notation in {'P','R','N','B','Q','K'}:
                        self.white.append(new_piece)
                    else:
                        self.black.append(new_piece)
        
    def in_check(self, color, board):
        attacked_squares = []
        attackers = self.black if color == "white" else self.white
        king_notation = "K" if color == "white" else "k"

        for piece in attackers:
            attacked_squares += piece.target_squares()

        return any(str(board[file][rank]) == king_notation for file, rank in attacked_squares)
    
    def promotion (self,board):
        promotion_boards = []
        for file in range(len(board)):
            print (file)
            if board[file][0] == 'p':
                print ('here')
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
                for notation in ['q','r','b','n']:
                    new_board = [file[:] for file in board]
                    new_board[file][0] = notation
                    promotion_boards.append(new_board)
            if board[file][7] == 'P':
<<<<<<< HEAD
=======
                print ('here1')
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
                for notation in ['Q','R','B','N']:
                    new_board = [new_file[:] for new_file in board]
                    new_board[file][7] = notation
                    promotion_boards.append(new_board)
        return promotion_boards
    
<<<<<<< HEAD
    def pawn_logic (self,piece,board):
=======
    def pawn_logic (self,piece):
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
        future_boards = []
        direction = 1 if piece.notation == 'P' else -1
        #jumps
        for distance in range (1,3):
            if distance == 2:
                if piece.color == 'white' and piece.rank != 1: 
                    break
                elif piece.color == 'black' and piece.rank != 6:
                    break #double jump only allowed on starting square
<<<<<<< HEAD
            if board[piece.file][piece.rank+(direction*distance)] == '_':
                new_board = [file[:] for file in board] #copy current board
=======
            print (piece.rank+(direction*distance))
            if self.board[piece.file][piece.rank+(direction*distance)] == '_':
                new_board = [file[:] for file in self.board] #copy current board
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[piece.file][piece.rank+(direction*distance)] = piece.notation
                legal = not self.in_check('white',new_board) if direction == 1 else not self.in_check('black',new_board)
                if legal:
                    if piece.rank+(direction*distance) == 7 and piece.color == 'white':
                        future_boards += self.promotion(new_board)
                    elif piece.rank+(direction*distance) == 0 and piece.color == 'black':
                        future_boards += self.promotion(new_board)
                    else:
                        future_boards.append (new_board)                  
            else:
                break
        #diagonal attacks
<<<<<<< HEAD
        for file,rank in piece.target_squares(board):
            enemy_piece = board[file][rank] in (self.black if direction == 1 else self.white)
            if enemy_piece:
                new_board = [file[:] for file in board] #copy current board
=======
        for file,rank in piece.target_squares():
            enemy_piece = self.board[file][rank] in (self.black if direction == 1 else self.white)
            if enemy_piece:
                new_board = [file[:] for file in self.board] #copy current board
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[file][rank] = piece.notation
                legal = not self.in_check('white',new_board) if direction == 1 else not self.in_check('black',new_board)
                if legal:
                    if rank == 7 and piece.color == 'white':
                        future_boards += self.promotion(new_board)
                    elif rank == 0 and piece.color == 'black':
                        future_boards += self.promotion(new_board)
                    else:
                        future_boards.append (new_board)    
        #taking en_passant
        if piece.en_passant_rights:
            new_file,new_rank = piece.en_passant_rights
<<<<<<< HEAD
            new_board = [file[:] for file in board] #copy current board
=======
            new_board = [file[:] for file in self.board] #copy current board
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
            new_board[piece.file][piece.rank] = '_'
            new_board[new_file][new_rank-direction] = '_'
            new_board[new_file][new_rank] = piece.notation
            legal = not self.in_check('white') if direction == 1 else not self.in_check('black')
            if legal:
                future_boards.append (new_board)
        return future_boards
        

    
<<<<<<< HEAD
    def castle_logic(self,king,board):
        future_boards = []
        #pieces that have moved can't castle
        #in check can't castle
        if self.king_has_moved[king.color] or self.in_check(king.color,board):
            return future_boards
        #short castle    
        if board[5][king.rank] == board[6][king.rank] == '_':
            rook = board[7][king.rank]
            if isinstance(rook,piece):
                if not self.rook_h_has_moved[king.color]:
                    for path in range (1,3):

                        new_board = [file[:] for file in board]
                        new_board[king.file][king.rank] = '_'
                        new_board[king.file+path][king.rank] = king.notation
                        legal = not self.in_check(king.color,new_board)
                        if not legal:
                            return future_boards
                        if path == 1:
                            new_board[king.file+path][king.rank] = '_'
                    new_board[5][king.rank] = new_board[7][king.rank]
                    new_board[7][king.rank] = '_'
                    future_boards.append(new_board)
        
        #long castle
        if board[3][king.rank] == board[2][king.rank] == board[1][king.rank] == '_':
            rook = board[0][king.rank]
            if isinstance(rook,piece):
                if not self.rook_a_has_moved[king.color]:
                    for path in range (-1,-3,-1):
                        new_board = [file[:] for file in board]
                        new_board[king.file][king.rank] = '_'
                        new_board[king.file+path][king.rank] = king.notation
                        legal = not self.in_check(king.color,new_board)
                        if not legal:
                            return future_boards
                        if path == -1:
                            new_board[king.file+path][king.rank] = '_'
                    new_board[3][king.rank] = new_board[0][king.rank]
                    new_board[0][king.rank] = '_'
                    future_boards.append(new_board)
                    
        return future_boards
        
    def find_legal_moves (self, color,board): #legal_moves are represented by the board positions
=======
    def castle_logic(self,piece):
        future_boards = []
        #pieces that have moved can't castle
        #in check can't castle
        if piece.has_moved or self.in_check(piece.color,self.board):
            return future_boards
        
        #short castle    
        if self.board[5][piece.rank] == self.board[6][piece.rank] == '_':
            if not self.board[7][piece.rank].has_moved and not piece.has_moved:
                for path in range (1,3):
                    new_board = [file[:] for file in self.board]
                    new_board[piece.file][piece.rank] = '_'
                    new_board[piece.file+path][piece.rank] = piece.notation
                    legal = not self.in_check(piece.color,new_board)
                    if not legal:
                        return future_boards
                    if path == 1:
                        new_board[piece.file+path][piece.rank] = '_'
                new_board[5][piece.rank] = new_board[7][piece.rank]
                new_board[7][piece.rank] = '_'
                future_boards.append(new_board)
            
        #long castle
        if self.board[3][piece.rank] == self.board[2][piece.rank] == self.board[1][piece.rank] == '_':
            if not self.board[0][piece.rank].has_moved and not piece.has_moved:
                for path in range (-1,-3,-1):
                    new_board = [file[:] for file in self.board]
                    new_board[piece.file][piece.rank] = '_'
                    new_board[piece.file+path][piece.rank] = piece.notation
                    legal = not self.in_check(piece.color,new_board)
                    if not legal:
                        return future_boards
                    if path == -1:
                        new_board[piece.file+path][piece.rank] = '_'
                new_board[3][piece.rank] = new_board[0][piece.rank]
                new_board[0][piece.rank] = '_'
                future_boards.append(new_board)
                    
        return future_boards
        
    def legal_moves (self, color): #legal_moves are represented by the board positions
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
        future_boards = []
        pieces = self.black if color == "black" else self.white
        for piece in pieces:
            if str(piece) in ['P','p']:
<<<<<<< HEAD
                future_boards += self.pawn_logic(piece,board) #pawn logic
                continue
            if str(piece) in ['K','k']:
                future_boards += self.castle_logic(piece,board)
            for move in piece.target_squares(board):
                new_board = [file[:] for file in board] #copy current board
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[move[0]][move[1]] = piece.notation #square moving to
                if move == (1,2):
                    for i in new_board:
                        file =[str(f) for f in i]
                        print (file)
=======
                future_boards += self.pawn_logic(piece) #pawn logic
                continue
            if str(piece) in ['K','k']:
                future_boards += self.castle_logic(piece)
            for move in piece.target_squares():
                new_board = [file[:] for file in self.board] #copy current board
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[move[0]][move[1]] = piece.notation #square moving to
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
                legal = not self.in_check(color,new_board)
                if legal:
                    future_boards.append(new_board)
        return future_boards
<<<<<<< HEAD

    def make_move (self,board):
        self.populate(board)
        
        rank = 0 if self.turn == 'white' else 7
        
        if str(board[4][rank]) not in ['R','r']:
            self.rook_a_has_moved[self.turn]= True
        if str(board[7][rank]) not in ['R','r']:
            self.rook_h_has_moved[self.turn] = True
        if str(board[4][rank]) not in ['K','k']:
            self.king_has_moved[self.turn] = True
        
        self.turn = 'white' if self.turn == 'black' else 'black'
        legal_moves = self.find_legal_moves(self.turn,board)
        
        if not legal_moves:
            if self.in_check(self.turn,board):
                self.turn = 'white' if self.turn == 'black' else 'black'
                self.turn += ' wins'
                print (self.turn)
            else:
                self.turn = 'stalemate'
                print (self.turn)
        
        
board3 = [
    ['B', 'K', '_', '_', 'P', 'p', '_', '_'],
    ['_', '_', 'Q', 'r', '_', '_', '_', '_'],
    ['_', '_', '_', 'k', '_', '_', '_', '_'],
    ['_', '_', '_', '_', '_', '_', '_', '_'],
    ['_', '_', 'P', 'p', '_', '_', '_', 'b'],
    ['_', '_', '_', 'N', 'B', '_', '_', '_'],
    ['_', '_', '_', '_', '_', '_', '_', '_'],
    ['_', '_', '_', 'P', '_', 'p', '_', '_']
    ]
        
import random
x = game()

print (x.in_check('white',board3))

x.find_legal_moves('white',x.board)

#1111


=======



x = game()
z = x.legal_moves('black')
for i in z:
    for s in i:
        print ([str(q) for q in s])
    print (999999999999)
>>>>>>> 2388261fee92fe0b7374a2e4d1f475ab61fba22b
