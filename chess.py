### globals ###
#colors
white = ['P','R','N','B','Q','K']
black = ['p','r','n','b','q','k']
#attack shapes
star = [(1,1),(-1,-1),(1,-1),(-1,1),(1,0),(-1,0),(0,-1),(0,1)]
diag = [(1,1),(-1,-1),(1,-1),(-1,1)]
straight = [(1,0),(0,1),(-1,0),(0,-1)]
L = [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)]
wp = [(1,1),(-1,1)]
bp = [(-1,-1),(1,-1)]
#mapping to pieces
attack_map = {
    'Q': star, 'K': star, 'q': star, 'k': star,
    'R': straight, 'r': straight,
    'B': diag, 'b': diag,
    'N': L, 'n': L,
    'P': wp,
    'p': bp
    }
standard2=[#1   2    3    4    5    6    7    8
        ['R', 'P', '_', '_', '_', '_', 'p', 'r'], #a
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'], #b
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'], #c
        ['Q', 'P', '_', '_', '_', '_', 'p', 'q'], #d
        ['K', 'P', '_', '_', '_', '_', 'p', 'k'], #e
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'], #f
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'], #g 
        ['R', 'P', '_', '_', '_', '_', 'p', 'r']  #h
        ]

#start board
standard=[#1   2    3    4    5    6    7    8
        ['R', 'P', '_', '_', '_', '_', 'p', 'r'], #a
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'], #b
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'], #c
        ['Q', '_', '_', '_', 'P', '_', 'p', 'q'], #d
        ['K', 'P', '_', '_', '_', '_', 'p', 'k'], #e
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'], #f
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'], #g 
        ['R', 'P', '_', '_', '_', '_', 'p', 'r']  #h
        ]


#test boards
board  =[#1    2    3    4    5    6    7    8
        ['_', '_', '_', '_', '_', '_', '_', 'r'], #a
        ['_', '_', '_', '_', '_', '_', '_', '_'], #b
        ['_', '_', '_', '_', '_', '_', '_', '_'], #c
        ['_', '_', '_', '_', '_', '_', '_', '_'], #d
        ['_', '_', '_', '_', '_', 'P', '_', 'k'], #e
        ['_', '_', '_', '_', '_', 'p', '_', '_'], #f
        ['_', '_', '_', '_', '_', 'P', '_', '_'], #g 
        ['_', '_', '_', '_', '_', '_', '_', 'r']  #h
        ]

board2 =[#1    2    3    4    5    6    7    8
        ['_', '_', '_', '_', '_', '_', '_', 'r'], #a
        ['_', '_', '_', '_', '_', '_', '_', '_'], #b
        ['_', '_', '_', '_', '_', '_', '_', '_'], #c
        ['_', '_', '_', '_', '_', '_', '_', '_'], #d
        ['_', '_', '_', '_', '_', 'P', '_', '_'], #e
        ['_', '_', '_', '_', '_', 'p', '_', 'r'], #f
        ['_', '_', '_', '_', '_', 'P', '_', 'k'], #g 
        ['_', '_', '_', '_', '_', '_', '_', '_']  #h
        ]


###game class###
class game:
    def __init__ (self,board):
        self.board = board
        self.moves = []
        self.flags = {
            'en_passant': None,
            'rook_a_moved': {'white': False, 'black': False},
            'rook_h_moved': {'white': False, 'black': False},
            'king_moved': {'white': False, 'black': False}
        }
        self.turn = 'white'
    
    def make_move(self,board,new_board):
        self.flags['en_passant'] = None
        
        self.board = new_board
        
        self.moves.append(move_notation(board,new_board))     
        
        for i in [ (0,'R','K','white'), (7,'r','k','black') ]:
            if new_board[0][i[0]] != i[1]:
                self.flags['rook_a_moved'][i[3]] = True
                return
            if new_board[7][i[0]] != i[1]:
                self.flags['rook_h_moved'][i[3]] = True
                return
            if new_board[4][i[0]] != i[2]:
                self.flags['king_moved'][i[3]] = True
                return
                
        new, missing = difference(board,new_board)
        new = new[0]
        missing = missing[0]
        if new_board[new[0]][new[1]] in ['P','p']:
            distance = missing[1] - new[1]
            if missing[0] == new[0] and distance in [2,-2]:
                self.flags['en_passant'] = (new[0],new[1]+(distance/2))

        
        

###standalone functions###
#return all squares being targeted by given square
def piece_targets(board,file,rank): 
    targets = []
    notation = board[file][rank]
    
    #one jump vs sliding pieces
    if notation in ['P','N','K','p','n','k']:
        distance = 1
    else: #['B','b','q','Q','r','R']
        distance = 8      
    #attack pattern
    attack_pattern = attack_map.get(notation)
    for delta_file, delta_rank in attack_pattern:
        for dist in range(distance):
            target_file = file + ((dist+1)*delta_file)
            target_rank = rank + ((dist+1)*delta_rank)
            if 8 > target_rank >= 0 and 8 > target_file >= 0:
                target = board[target_file][target_rank]
                if target != '_':
                    if notation in white and target in black:
                        targets.append((target_file,target_rank))
                    if notation in black and target in white:
                        targets.append((target_file,target_rank))
                    break
                else:
                    pass
                    targets.append((target_file,target_rank))
            else:
                break
    return targets


def in_check(board,color):
    attacked_squares = []
    attackers = black if color == 'white' else white
    king = 'K' if color == 'white' else 'k'
    for file in range(len(board)):
        for rank in range(len(board[file])):
            occupant = board[file][rank]
            if occupant in attackers:
                attacked_squares += piece_targets(board,file,rank)
            if occupant == king:
                king = (file,rank)
    if king in attacked_squares:
        return True
    else:
        return False
    
def valid_check(board,file,rank,new_file,new_rank):
    notation = board[file][rank]
    board = [file[:] for file in board]#copy board
     #grab notation
    board[file][rank] = '_'
    board[new_file][new_rank] = notation
    color = 'white' if notation in white else 'black'

    if not in_check(board,color):
        return board
    else:
        return []
    
def promotion(board,file,rank):
    boards = []
    notation = board[file][rank]
    pieces = ['Q','R','B','N'] if notation == 'P' else ['q','r','b','n']
    for i in pieces:
        new_board = [file[:] for file in board]
        new_board[file][rank] = i
        boards.append( new_board)
    return boards

def pawn_logic(board,file,rank,flags): #returns all legal moves for a pawn piece
    boards = []
    notation = board[file][rank]
    direction = 1 if notation == 'P' else -1
    #regular jumps
    if board[file][rank+direction] == '_':
        one_jump = valid_check(board,file,rank,file,rank+direction)
        if one_jump:
            if rank+direction in [0,7]:
                boards += promotion(one_jump,file,rank+direction)
            else:
                boards.append(one_jump)
        if notation in white and rank == 1 or notation in black and rank == 6: #on start rank
            if board[file][rank+(direction*2)] == '_':
                two_jump = valid_check(board,file,rank,file,rank+(direction*2))
                if two_jump:
                    boards.append(two_jump)

    #captures
    for new_file,new_rank in piece_targets(board,file,rank):
        target = board[new_file][new_rank]
        if notation in white and target in black or notation in black and target in white:
            capture = valid_check(board,file,rank,new_file,new_rank)
            if capture:
                if new_rank in [0,7]:
                    boards += promotion(capture,new_file,new_rank)
                else:
                    boards.append(capture)
                    
    #capture en passant
    for i in [-1,1]:
        new_file = file + i
        if not 0 <= new_file < 8:
            continue
        new_rank = rank + direction
        target = board[new_file][new_rank]
        if (new_file,new_rank) == flags['en_passant']:
            new_board = [file[:] for file in board]
            new_board[new_file][rank] = '_'
            capture = valid_check(new_board,file,rank,new_file,new_rank)
            if capture:
                boards.append(capture)            
    return boards

def king_logic(board,file,rank,flags): #returns all legal moves for a king piece
    boards = []
    notation = board[file][rank]
    color = 'white' if notation in white else 'black'
    if not flags['king_moved'][color] and not in_check(board,color): #kings not in check or moved yet
        #long castle
        if not flags['rook_a_moved'][color]: # rook a not moved
            if board[1][rank] == board[2][rank] == board[3][rank] == '_' and board[0][rank] in ['r','R']: #path clear
                for i in range (1,3):
                    new_board = [file[:] for file in board]
                    new_board = valid_check(new_board,file,rank,file-i,rank) #path safe
                    if not new_board:
                        break
                    if i == 2:#made it this far, means all clear
                        new_board[3][rank] = new_board[0][rank] 
                        new_board[0][rank] = '_'
                        boards.append(new_board)
        #short castle
        if not flags['rook_h_moved'][color]: #rook h not moved       
            if board[5][rank] == board[6][rank] == '_' and board[7][rank] in ['r','R']:#path clear
                for i in range (1,3):
                    new_board = [file[:] for file in board]
                    new_board = valid_check(new_board,file,rank,file+i,rank)#path safe
                    if not new_board:
                        break
                    if i == 2:#made it this far, means all clear
                        new_board[5][rank] = new_board[7][rank] 
                        new_board[7][rank] = '_'
                        boards.append(new_board)
    
    #regular moves      
    for new_file,new_rank in piece_targets(board,file,rank):
        target = board[new_file][new_rank]
        if notation in white and target in black or notation in black and target in white or target == '_':
            move = valid_check(board,file,rank,new_file,new_rank)
            if move:
                boards.append(move)

        
    return boards

def legal_moves(board,color,flags):
    boards = []
    pieces = white if color == 'white' else black
    for file in range(len(board)):
        for rank in range(len(board[file])):
            occupant = board[file][rank]
            if occupant in pieces and occupant in ['P','p']:
                pawn_moves = (pawn_logic(board,file,rank,flags))
                if pawn_moves:
                    boards += pawn_moves
            elif occupant in pieces and occupant in ['K','k']:
                boards += king_logic(board,file,rank,flags)
                
            elif occupant in pieces and occupant not in ['R','r']:
                targets = piece_targets(board,file,rank)
                for new_file, new_rank in targets:
                    new_board = valid_check(board,file,rank,new_file,new_rank)
                    if new_board:
                        boards.append(new_board)
    return boards
                    
                    
def move_notation(board,new_board):
    extra = '' #check/ checkmate
    files = ['a','b','c','d','e','f','g','h']
    ranks = ['1','2','3','4','5','6','7','8']
    
    new, missing = difference(board,new_board)
                    
    #is new board a check or checkmate
    moved_color = 'white' if new_board[new[0][0]][new[0][1]] in white else 'black'
    opp_color = 'black' if moved_color == 'white' else 'white'
    
    #other player in check?
    if in_check(new_board,opp_color):
        print ('check delivered')
        if legal_moves(new_board,opp_color): #check
            extra = '+'
        else:#checkmate
            extra = '#'
            print ('checkmate')
    
    #castle
    if len(new) > 1: #two pieces in new locations 
        if new[0][0] in [2,3]: #long castle
            return 'O-O-O' + extra
        elif new[0][0] in [6,5]: #short castle
            return 'O-O' + extra
    
    #en passant
    if len(missing) > 1: #two pieces not in old location and not castle
        targ_file = new[0][0]
        for i in missing:
            if i[0] != targ_file:
                origin_file = i[0] 
        origin_file = files[origin_file]
        targ_file = files[targ_file]
        return origin_file + 'x' + targ_file + str(new[0][1]+1) + extra
    
    #captures + non captures
    notation = new_board[new[0][0]][new[0][1]]
    old_occupant = board[new[0][0]][new[0][1]]
    attacker = new_board[new[0][0]][new[0][1]]
    same_pieces = []
    new_file = files[new[0][0]]
    new_rank = ranks[new[0][1]] #no need to differentiate FIX IT ########################
    #check if any identical pieces
    #print (notation)
    for file in range(len(board)):
        for rank in range(len(board[file])):
            if board[file][rank] == notation and (file,rank) != (missing[0][0],missing[0][1]): #same piece somewhere
                same_pieces.append((file,rank))

    attackers = []
    for i in same_pieces:
        targets = piece_targets(board,i[0],i[1])
        if new[0] in targets:
            attackers.append(i)
    if not attackers: #
        print ('no differentiation neccessary')
        if old_occupant != '_':
            return notation + 'x' + new_file + new_rank + extra
        else:
            return notation + new_file + new_rank + extra
        
    for i in attackers:
        if i[0] == missing[0][0]: #file is not enough to differentiate
            print ('file is not enough to differentiate')
            break
    else:
        print ('differentiated by file')
        if old_occupant != '_':
            return attacker + files[missing[0][0]] + "x" + new_file + new_rank +extra#differentiated by file
        else:
            return attacker + files[missing[0][0]] + new_file + new_rank + extra#differentiated by file
    for i in same_pieces:
        if i[1] == missing[0][1]: #rank is not enough to differentiate
            print ('rank is not enough to differentiate')
            break
    else:
        print ('#differentiated by rank')
        if old_occupant != '_':
            return attacker + ranks[missing[0][1]] + "x" + new_file + new_rank + extra #differentiated by file
        else:
            return attacker + ranks[missing[0][1]] + new_file + new_rank + extra#differentiated by file
    
    print ('double disambiguation')
    if old_occupant != '_':
        return attacker + files[missing[0][0]] + ranks[missing[0][1]] + "x" + new_file + new_rank + extra
    else:
        return attacker + files[missing[0][0]] + ranks[missing[0][1]] + new_file + new_rank + extra
        
def difference(old_board,new_board):
    new = []
    missing = []
    for file in range(len(board)):
        for rank in range(len(board[file])):
            old_square_state = board[file][rank]
            new_square_state = new_board[file][rank]
            if new_square_state != old_square_state: #find change between boards
                if new_board[file][rank] == '_': #square empty that had a piece before
                    missing.append((file,rank))
                else:
                    new.append((file,rank)) #piece in location it wasn't before
    return new,missing
                    

        
new1 = game(standard)

#x = legal_moves(new1.board,new1.turn,new1.flags)
new1.make_move(board,board2)

