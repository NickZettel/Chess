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
            
        #pawn parameters
        self.has_moved = False
        self.en_passant_rights = False
            
        #string representation
    def __str__ (self):
        return self.notation
    
    #returns squares the piece is currently attacking
    def target_squares (self): 
        targets = []
        for delta_file, delta_rank in self.attack_pattern:
            for dist in range(self.distance):
                target_file = self.file + ((dist+1)*delta_file)
                target_rank = self.rank + ((dist+1)*delta_rank)
                if 8 > target_rank >= 0 and 8 > target_file >= 0:
                    target = str(self.board[target_file][target_rank])
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
        return targets
    

class game:
    def __init__ (self):
        self.white = []
        self.black = []
        self.board = [
        ['R', 'P', '_', '_', '_', '_', 'p', 'r'],
        ['_', 'P', '_', '_', '_', '_', 'p', 'n'],
        ['_', 'P', '_', '_', '_', '_', 'p', 'b'],
        ['_', 'P', '_', '_', '_', '_', 'p', 'q'],
        ['K', 'P', '_', '_', '_', '_', 'p', 'k'],
        ['_', '_', '_', 'q', 'p', '_', 'p', 'b'],
        ['_', 'P', '_', '_', 'P', '_', 'p', 'n'],
        ['R', 'P', '_', '_', 'p', '_', 'p', 'r']
        ]
        
        
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
        
        self.board[6][4].en_passant_rights = (7,5)
        
    def in_check(self, color):
        attacked_squares = []
        attackers = self.black if color == "white" else self.white
        king_notation = "K" if color == "white" else "k"

        for piece in attackers:
            attacked_squares += piece.target_squares()

        return any(str(self.board[file][rank]) == king_notation for file, rank in attacked_squares)
    
    def pawn_logic (self,piece):
        future_boards = []
        direction = 1 if piece.notation == 'P' else -1
        for distance in range (1,3):
            if self.board[piece.file][piece.rank+direction*distance] == '_':
                new_board = [file[:] for file in self.board] #copy current board
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[piece.file][piece.rank+direction*distance] = piece.notation
                break
                legal = not self.in_check('white') if direction == 1 else not self.in_check('black')
                if legal:
                    future_boards.append (new_board)                    
            else:
                break
        for file,rank in piece.target_squares():
            enemy_piece = str(self.board[file][rank]) in (self.black if direction == 1 else self.white)
            if enemy_piece:
                new_board = [file[:] for file in self.board] #copy current board
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[file][rank] = piece.notation
                legal = not self.in_check('white') if direction == 1 else not self.in_check('black')
                break
                if legal:
                    future_boards.append (new_board)
        
        if piece.en_passant_rights:
            new_file,new_rank = piece.en_passant_rights
            new_board = [file[:] for file in self.board] #copy current board
            new_board[piece.file][piece.rank] = '_'
            new_board[new_file][new_rank-direction] = '_'
            new_board[new_file][new_rank] = piece.notation
            legal = not self.in_check('white') if direction == 1 else not self.in_check('black')
            if legal:
                future_boards.append (new_board)
        return future_boards
    
    def castle_logic(self,piece):
        future_boards = []
        #pieces that have moved can't castle
        #in check can't castle
        if piece.has_moved or self.in_check(piece.color):
            return future_boards
        
        #short castle    
        if self.board[5][piece.rank] == '_' and self.board[6][piece.rank] == '_' and not self.board[7][piece.rank].has_moved:
            for path in range (1,3):
                new_board = [file[:] for file in self.board]
                new_board[piece.file][piece.rank] = '_'
                new_board[piece.file+path][piece.rank] = piece.notation
                legal = not self.in_check(piece.color)
                if not legal:
                    return future_boards
                if path == 1:
                    new_board[piece.file+path][piece.rank] = '_'
            new_board[5][piece.rank] = new_board[7][piece.rank]
            new_board[7][piece.rank] = '_'
            new_board[6][piece.rank] = piece.notation
            future_boards.append(new_board)
        return future_boards
        
    def legal_moves (self, color): #legal_moves are represented by the board positions
        future_boards = []
        pieces = self.black if color == "black" else self.white
        for piece in pieces:
            if str(piece) in ['P','p']:
                future_boards += self.pawn_logic(piece) #pawn logic
                continue
            if str(piece) in ['K','k']:
                future_boards += self.castle_logic(piece)
            for move in piece.target_squares():
                new_board = [file[:] for file in self.board] #copy current board
                new_board[piece.file][piece.rank] = '_' #square left behind
                new_board[move[0]][move[1]] = piece.notation #square moving to
                legal = not self.in_check(color)
                if legal:
                    future_boards.append(new_board)
        return future_boards



x = game()
z = x.legal_moves('white')
for i in z:
    for s in i:
        print ([str(q) for q in s])
    print (999999999999)



class game:
    def __init__ (self,pieces, turn = white):
        self.pieces = pieces
        self.turn = turn
        
    def legal_next_positions (self):
        for i in pieces:
            if i in self.turn:
                pass


    
class king(piece):
    def __init__(self, pointer_to_board , file, rank, piece_notation):
        super().__init__(pointer_to_board , file, rank, piece_notation)
    
class queen(piece):
    def __init__(self, pointer_to_board , file, rank, piece_notation):
        super().__init__(pointer_to_board , file, rank, piece_notation)
   
class rook(piece):
    def __init__(self, pointer_to_board , file, rank, piece_notation):
        super().__init__(pointer_to_board , file, rank, piece_notation)

class bishop(piece):
    def __init__(self, pointer_to_board , file, rank, piece_notation):
        super().__init__(pointer_to_board , file, rank, piece_notation)

class knight(piece):
    def __init__(self, pointer_to_board , file, rank, piece_notation):
        super().__init__(pointer_to_board , file, rank, piece_notation)

class pawn(piece):
    def __init__(self, pointer_to_board , file, rank, piece_notation):
        super().__init__(pointer_to_board , file, rank, piece_notation)






class rules:
    white = ['P','R','N','B','Q','K']
    black = ['p','r','n','b','q','k']
    
    star = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,-1),(0,1)]
    diag = [(1,1),(-1,-1),(1,-1),(-1,1)]
    straight = [(1,0),(0,1),(-1,0),(0,-1)]
    L_shaped = [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)]
    wp = [(1,1),(-1,1)]
    bp = [(-1,-1),(1,-1)]

    attack_patterns = {
        'k': star,
        'q': star,
        'b': diag,
        'r': straight,
        'n': L_shaped,
        'K': star,
        'Q': star,
        'B': diag,
        'R': straight,
        'N': L_shaped,
        'P': wp,
        'p': bp
    }

    
    def piece_targets (board, file, rank, attack_pattern): 
        attacking = []
        piece = board[file][rank]
        
        if piece == '_':
            return attacking
        
        if piece in ['P','N','K','p','n','k']:
            distance = 1
        else:
            distance = 8

        for delta_file, delta_rank in attack_pattern:
            for dist in range(distance):
                new_file = file + ((dist+1)*delta_file)
                new_rank = rank + ((dist+1)*delta_rank)
                if 8 > new_rank >= 0 and 8 > new_file >= 0:
                    if board[new_file][new_rank] != '_':
                        attacking.append(board[new_file][new_rank])
                        break
                else:
                    break
        return attacking
    
    def all_targets (board,attacking_pieces): #get all attacks from a list of pieces
        attacked = []
        for file in range(len(board)):
            for rank in range(len(board[file])):
                piece = board[file][rank]
                if piece in attacking_pieces:
                    attacked += rules.piece_targets(board,file,rank,rules.attack_patterns[piece])
        return attacked
    
    def legal_pawn_jumps(board, file, rank):
        potential_boards = []
        piece = board[file][rank]

        if piece not in ['P', 'p']:  # Only handle pawns
            return jumps

        direction = 1 if piece == 'P' else -1  # White moves up, Black moves down

        for i in range(1, 3):  # Pawns can jump one or two spaces forward
            if i == 2 and piece == 'P' and rank != 1:
                break
            elif i == 2 and piece == 'p' and rank != 6:
                break
            
            new_rank = rank + direction * i

            if not (0 <= new_rank < 8):  # Out of bounds check
                break
            
            if board[file][new_rank] != '_':  # Blocked by a piece
                break  

            new_board = [copied_list[:] for copied_list in board]
            new_board[file][rank] = '_'
            new_board[file][new_rank] = piece

            if (piece == 'P' and rules.kings_in_check(new_board)[0]):
                break
            if (piece == 'p' and rules.kings_in_check(new_board)[1]):
                break  

            potential_boards.append(new_board)  

        return potential_boards
                

    
    def legal_moves(board,file,rank):
        piece = board[file][rank]
                
        squares = []
        potential_boards = []
        
        if piece == '_':
            return squares
        if piece in ['P','N','K','p','n','k']:
            distance = 1
        else:
            distance = 8

        for delta_file,delta_rank in rules.attack_patterns[piece]:
            for dist in range(distance):
                
                new_file = file + ((dist+1)*delta_file)
                new_rank = rank + ((dist+1)*delta_rank)
                
                if 8 > new_rank >= 0 and 8 > new_file >= 0:
                    pass
                else:
                    break
                
                new_square_occupant = board[new_file][new_rank]
                
                if piece in rules.white and new_square_occupant in rules.white:
                    break
                
                elif piece in rules.black and new_square_occupant in rules.black:
                    break
                
                new_board = [copied_list[:] for copied_list in board]
                
                new_board[file][rank] = '_'
                new_board[new_file][new_rank] = piece
                
                if piece in rules.white and rules.kings_in_check(new_board)[0]:
                    break
                
                elif piece in rules.black and rules.kings_in_check(new_board)[1]:
                    break
                
                if piece == 'p' and new_square_occupant in rules.white:
                    squares.append((new_file,new_rank))
                    break
                elif piece == 'P' and new_square_occupant in rules.black:
                    squares.append((new_file,new_rank))
                    break
                elif piece in ['P','p']:
                    break
                
                squares.append((new_file,new_rank))
                potential_boards.append(new_board)
                
                if new_square_occupant != '_' :
                    break
       
        if piece in ['p','P']:
            potential_boards += rules.legal_pawn_jumps(board,file,rank)
          
        return potential_boards
                
                    
                            
    def kings_in_check (board):
        white_king_in_check = True if 'K' in rules.all_targets(board,rules.black) else False
        black_king_in_check = True if 'k' in rules.all_targets(board,rules.white) else False
        return (white_king_in_check,black_king_in_check)
    
#possible_moves =rules.legal_moves(rules.standard_game,2,6)
#for i in possible_moves:
 #   for j in i:
  #      print (j)
  #  print ('%%%%%%%%%%%%%%%')


    