import pygame

import os
import chess_logic
# --- Globals ---
#screen location
os.environ['SDL_VIDEO_WINDOW_POS'] = "2000,100"
pygame.init()

#text options and surfaces
font = pygame.font.SysFont('Aptos', 30)
orientation_text = font.render('Reverse POV', False, (0, 0, 0))

#screen size
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

#window title and icon
pygame.display.set_caption("chess_logic")
icon = pygame.image.load("icon.png")  # Replace with your image file path
pygame.display.set_icon(icon)

#menu item coordinates
pov_x = 635
pov_y = 560
pov_width = 130
pov_height = 20


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


#menu valiables
hover_pov = False

#--- game variables---
board1 = chess_logic.game(chess_logic.standard)
held_piece = None
board_orientation = 'Left'
origin = [0,0] #where board appears on the screen
promotion = False
orientation = 0 #1 means white on bottom, 0 means black on bottom
board_width = width-200
board_height = height


#Standard starting board
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

#make pieces fit screen
def scale_images(images,height,width):
    for key in images:
        images[key] = pygame.transform.scale(images[key], (height,width))

def draw_pieces(board):
    tile_width = board_width / 8
    tile_height = board_height / 8
    for file in range(8): #loop through board
        for rank in range(8):
            notation = board[file][rank]
            if notation in piece_images and (file, rank) != held_piece:  # If there's a piece, draw it
                if orientation: #white on bottom
                    x = origin[0] + (file * tile_width)
                    y = origin[1] + ((7 - rank) * tile_height)                
                    screen.blit(piece_images[notation], (x, y))
                else: #black on bottom
                    x = board_width - (file * tile_width) - tile_width
                    y = board_height - ((7 - rank) * tile_height) - tile_height               
                    screen.blit(piece_images[notation], (x, y))

def draw_board():
    tile_width = board_width / 8
    tile_height = board_height / 8

    for file in range(8):
        for rank in range(8):
            color = white if (file + rank) % 2 == 0 else blue
            x = origin[0] + (file * tile_width)
            y = origin[1] + (rank * tile_height)
            pygame.draw.rect(screen, color, (x, y, tile_width, tile_height))

def square_clicked(pos):
    if orientation:
        file = pos[0] // (board_width // 8)
        rank = 7 - (pos[1] // (board_height // 8))
    else:
        file = 7 - (pos[0] // (board_width // 8))
        rank = (pos[1] // (board_height // 8))
    return (file,rank)

def draw_promotion_menu():
    menu_x_origin = board_width/4
    menu_y_origin = board_height/2 - board_height/8/2
    menu_height = board_height/8
    menu_width = board_width/2
    pygame.draw.rect(screen, black, (menu_x_origin,menu_y_origin, menu_width,menu_height))
    pos = pygame.mouse.get_pos()
    if menu_x_origin < pos[0] < menu_x_origin + board_width/2 and menu_y_origin < pos[1] <menu_y_origin + board_height/8:
        x = int((pos[0]-menu_x_origin) / (board_width/8))
        if x in [0,1,2,3]:
            pygame.draw.rect(screen, yellow, (menu_x_origin+ (x * board_width/8),menu_y_origin, board_width/8,board_height/8))
    promotion_list = ['Q','R','B','N'] if promotion[1] == 7 else ['q','r','b','n']
    for i in range(len(promotion_list)):
        screen.blit(piece_images[promotion_list[i]], (menu_x_origin+ board_width/8 * i, menu_y_origin ))
    if orientation:
        pawn_x = promotion[0] * board_width /8
        pawn_y = board_height - (promotion[1] * board_height /8) - (board_height/8)
    else:
        pawn_x = board_width - (promotion[0] * board_width /8) - (board_width/8)
        pawn_y = (promotion[1] * board_height /8)
    screen.blit(piece_images['P'], (pawn_x,pawn_y)) if promotion[1] == 7 else screen.blit(piece_images['p'], (pawn_x,pawn_y))


def draw_orientation_button():
    if hover_pov:
        pygame.draw.rect(screen, white, (pov_x, pov_y, pov_width, pov_height))
        screen.blit(orientation_text, (pov_x,pov_y))
    else:
        pygame.draw.rect(screen, blue, (pov_x, pov_y, pov_width, pov_height))
        screen.blit(orientation_text, (pov_x,pov_y))

def check_pov_hover(pos):
    global hover_pov
    x,y = pos
    if pov_x + pov_width > x > pov_x and pov_y +pov_height > y > pov_y:
        hover_pov = True
    else:
        hover_pov = False

#pre game settings
scale_images(piece_images,board_width/8,board_height/8)
i = 0
running = True
while running:
    i += 1
    pygame.display.set_caption(str(i))
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and hover_pov:
            orientation = 1 if orientation == 0 else 0
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not promotion:
            file, rank = square_clicked(pos)
            print (file,rank)
            if 0<=file<8 and 0<=rank<8:
                print ('here2')
                if board1.board[file][rank] != '_' and pos[0]<board_width and pos[1]< board_height:
                    print ('here')
                    held_piece = (file,rank)
                    print (held_piece)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and promotion:
            menu_x_origin = board_width/4
            menu_y_origin = board_height/2 - board_height/8/2
            if menu_x_origin < pos[0] < menu_x_origin + board_width/2 and menu_y_origin < pos[1] <menu_y_origin + board_height/8: #click in menu
                x = int((pos[0]-menu_x_origin) / (board_width/8))
                legal_moves = chess_logic.legal_moves(board1.board,board1.turn, board1.flags)
                promotion_list = ['Q','R','B','N'] if promotion[1] == 7 else ['q','r','b','n']
                for board in legal_moves:
                    if board[promotion[0]][promotion[1]] == promotion_list[x]:
                        board1.make_move(board1.board,board)
                        held_piece = None
                        promotion = False
                        break  
                
        if event.type == pygame.MOUSEBUTTONUP and not promotion:
            file, rank = square_clicked(pos)
            
            if (file,rank) == held_piece: #dropped on original square
                held_piece = None
            
            for i in [file,rank]: #dropped outside board
                if i < 0 or i > 7:
                    held_piece = None
            
            if held_piece:
                legal_moves = chess_logic.legal_moves(board1.board,board1.turn, board1.flags)
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
    draw_orientation_button()
    
    check_pov_hover(pos)
    if held_piece and not promotion:
        x,y = pygame.mouse.get_pos()
        notation = board1.board[held_piece[0]][held_piece[1]]
        offset_x = width/8/2
        offset_y = height/8/2
        screen.blit(piece_images[notation], (x-offset_x, y-offset_y))
        
    if promotion: #display promotion selection menu
        draw_promotion_menu()
    pygame.display.update()
    
pygame.quit()