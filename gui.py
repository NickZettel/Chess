import pygame
import os
import Chess
# --- Globals ---
#screen location
os.environ['SDL_VIDEO_WINDOW_POS'] = "2000,100"
pygame.init()

#screen size
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

#window title and icon
pygame.display.set_caption("Chess")
icon = pygame.image.load("icon.png")  # Replace with your image file path
pygame.display.set_icon(icon)

#colors
white = (255,255,255)
black = (0,0,0)
blue = ("#275b9c")
grey = (155,155,155)
yellow = (155,155,0)

#piece images
piece_images = {}
piece_images["P"] = pygame.image.load("white_pawn.png")
piece_images["N"] = pygame.image.load("white_knight.png")
piece_images["B"] = pygame.image.load("white_bishop.png")
piece_images["R"] = pygame.image.load("white_rook.png")
piece_images["Q"] = pygame.image.load("white_queen.png")
piece_images["K"] = pygame.image.load("white_king.png")

piece_images["p"] = pygame.image.load("black_pawn.png")
piece_images["n"] = pygame.image.load("black_knight.png")
piece_images["b"] = pygame.image.load("black_bishop.png")
piece_images["r"] = pygame.image.load("black_rook.png")
piece_images["q"] = pygame.image.load("black_queen.png")
piece_images["k"] = pygame.image.load("black_king.png")

#--- oopable variables ---
board1 = Chess.game(Chess.standard)
held_piece = None
board_orientation = 'Left'
origin = [0,0]
promotion = False



standard=[#1   2    3    4    5    6    7    8
        ['R', 'P', '_', '_', '_', '_', 'p', 'r'], #a
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'], #b
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'], #c
        ['Q', 'P', '_', '_', '_', '_', 'p', 'q'], #d
        ['K', 'P', '_', '_', '_', '_', 'p', 'k'], #e
        ['B', 'P', '_', '_', '_', '_', 'p', 'b'], #f
        ['N', 'P', '_', '_', '_', '_', 'p', 'n'], #g 
        ['R', 'P', '_', '_', '_', '_', 'p', 'r']  #h
        ]

def scale_images(images,height,width):
    for key in images:
        images[key] = pygame.transform.scale(images[key], (height,width))
        
        
def draw_pieces(board):
    tile_width = width / 8
    tile_height = height / 8
    
    for file in range(8):
        for rank in range(8):
            notation = board[file][rank]
            if notation in piece_images and (file, rank) != held_piece:  # If there's a piece, draw it
                x = origin[0] + (file * tile_width)
                y = origin[1] + ((7 - rank) * tile_height)                
                screen.blit(piece_images[notation], (x, y))


def draw_board():
    tile_width = width / 8
    tile_height = height / 8

    for file in range(8):
        for rank in range(8):
            color = white if (file + rank) % 2 == 0 else blue
            x = origin[0] + (file * tile_width)
            y = origin[1] + (rank * tile_height)
            pygame.draw.rect(screen, color, (x, y, tile_width, tile_height))

def square_clicked(pos):
    file = pos[0] // (width // 8)
    rank = 7 - (pos[1] // (height // 8))
    return (file,rank)

#pre game settings
scale_images(piece_images,width/8,height/8)
i = 0
running = True
while running:
    i += 1
    pygame.display.set_caption(str(i))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not promotion:
            pos = pygame.mouse.get_pos()
            file, rank = square_clicked(pos)
            if board1.board[file][rank] != '_':
                held_piece = (file,rank)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and promotion:
            pos = pygame.mouse.get_pos()
            menu_x_origin = width/4
            menu_y_origin = height/2 - height/8/2
            if menu_x_origin < pos[0] < menu_x_origin + width/2 and menu_y_origin < pos[1] <menu_y_origin + height/8:
                x = int((pos[0]-menu_x_origin) / (width/8))
                legal_moves = Chess.legal_moves(board1.board,board1.turn, board1.flags)
                promotion_list = ['Q','R','B','N'] if promotion[1] == 7 else ['q','r','b','n']
                for board in legal_moves:
                    if board[promotion[0]][promotion[1]] == promotion_list[x]:
                        print ('here',board, 'b1',board1.board)
                        board1.make_move(board1.board,board)
                        held_piece = None
                        promotion = False
                        break
            
                
        if event.type == pygame.MOUSEBUTTONUP and not promotion:
            pos = pygame.mouse.get_pos()
            file, rank = square_clicked(pos)
            
            if (file,rank) == held_piece: #dropped on original square
                held_piece = None
            
            for i in [file,rank]: #dropped outside board
                if i < 0 or i > 7:
                    held_piece = None
            
            if held_piece:
                legal_moves = Chess.legal_moves(board1.board,board1.turn, board1.flags)
                notation = board1.board[held_piece[0]][held_piece[1]]
                for board in legal_moves:
                    new_square = board[file][rank]
                    old_square = board[held_piece[0]][held_piece[1]]
                    if new_square == notation and old_square == '_': #valid move
                        if notation in ['R','r'] and board1.board[4][held_piece[1]] in ['K','k'] and board[4][held_piece[1]] == '_':
                            continue #don't let rooks perform castle
                        else:   
                            board1.make_move(board1.board,board)
                            held_piece = None
                        break
                    elif old_square == '_' and notation in ['p','P'] and new_square in ['Q','q','r','R','B','b','n','N']:
                        if board1.board[file][rank] != board[file][rank]:
                            promotion = (file,rank)
                            break
            if not promotion:
                held_piece = None

            
    
    screen.fill(black)
    draw_board()
    draw_pieces(board1.board)
    if held_piece and not promotion:
        x,y = pygame.mouse.get_pos()
        notation = board1.board[held_piece[0]][held_piece[1]]
        offset_x = width/8/2
        offset_y = height/8/2
        screen.blit(piece_images[notation], (x-offset_x, y-offset_y))
        
    if promotion: #display promotion selection menu
        menu_x_origin = width/4
        menu_y_origin = height/2 - height/8/2
        menu_height = height/8
        menu_width = width/2
        pygame.draw.rect(screen, black, (menu_x_origin,menu_y_origin, menu_width,menu_height))
        pos = pygame.mouse.get_pos()
        if menu_x_origin < pos[0] < menu_x_origin + width/2 and menu_y_origin < pos[1] <menu_y_origin + height/8:
            x = int((pos[0]-menu_x_origin) / (width/8))
            if x in [0,1,2,3]:
                pygame.draw.rect(screen, yellow, (menu_x_origin+ (x * width/8),menu_y_origin, width/8,height/8))
        promotion_list = ['Q','R','B','N'] if promotion[1] == 7 else ['q','r','b','n']
        for i in range(len(promotion_list)):
            screen.blit(piece_images[promotion_list[i]], (menu_x_origin+ width/8 * i, menu_y_origin ))
        pawn_x = promotion[0] * width /8
        pawn_y = height - (promotion[1] * height /8) - (height/8)
        screen.blit(piece_images['P'], (pawn_x,pawn_y)) if promotion[1] == 7 else screen.blit(piece_images['p'], (pawn_x,pawn_y))
    pygame.display.update()
    
pygame.quit()