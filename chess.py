import random
class piece:
    def __init__ (self, pointer_to_board,piece_notation,file,rank):
        self.str = piece_notation
        self.board = pointer_to_board
    def __str__ (self):
        return self.str

class player:
    def __init__ (self):
        self.pieces = []


class rules:
    standard_game = [
        ['R', 'P', '_', '_', '_', '_', 'p', 'r'],
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'],
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'],
        ['Q', 'P', '_', '_', '_', '_', 'p', 'q'],
        ['K', 'P', '_', '_', '_', '_', 'p', 'k'],
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'],
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'],
        ['R', 'P', '_', '_', '_', '_', 'p', 'r']
        ]
    
    white = ['P','R','N','B','Q','K']
    black = ['p','r','n','b','q','k']
    
    star = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,-1),(0,1)]
    diag = [(1,1),(-1,-1),(1,-1),(-1,1)]
    straight = [(1,0),(0,1),(-1,0),(0,-1)]
    el = [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)]
    wp = [(1,1),(-1,1)]
    bp = [(-1,-1),(1,-1)]

    attack_patterns = {
        'k': star,
        'q': star,
        'b': diag,
        'r': straight,
        'n': el,
        'K': star,
        'Q': star,
        'B': diag,
        'R': straight,
        'N': el,
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
    
possible_moves =rules.legal_moves(rules.standard_game,0,1)
for i in possible_moves:
    for j in i:
        print (j)
    print ('%%%%%%%%%%%%%%%')


    