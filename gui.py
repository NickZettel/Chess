from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QGridLayout,QSizePolicy, QListWidget,QVBoxLayout
\
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import Chess


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Board Game Selector")
        self.resize(300, 200)

        # --- Main Menu ---
        layout = QVBoxLayout(self)
        title = QLabel("Board Games")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        chess_button = QPushButton("Play Chess")
        chess_button.clicked.connect(self.open_chess)

        layout.addWidget(title)
        layout.addWidget(chess_button)
        layout.addStretch()  # Push everything up

        self.chess_window = None  # Track game window

    def open_chess(self):
        if not self.chess_window or not self.chess_window.isVisible():
            self.chess_window = ChessBoard()
            self.chess_window.show()
            

class ChessBoard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chess")
        self.resize(500, 400)
        
        self.game = Chess.game(Chess.standard)
        
        layout = QHBoxLayout(self)

        board = self.create_chessboard()
        settings = self.create_menu()
        
        layout.addWidget(board,3)
        layout.addWidget(settings,1)

    def create_menu(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        layout.setSpacing(5)
        
        title = QLabel("Move List")
        layout.addWidget(title)
        
        label = QLabel("Hello")
        
        self.list_widget = QListWidget()
        #self.list_widget.addItems([f"Item {i}" for i in range(1, 51)])
        
        layout.addWidget(self.list_widget)
        layout.addWidget(label)
        return container
        
    
    def create_chessboard(self):
        """Creates an 8x8 chessboard with no pieces."""
        board_container = QWidget()
        squares = QGridLayout(board_container)
        squares.setSpacing(0)
        
        white_square = QPixmap("white_square.png")
        black_square = QPixmap("black_square.png")
        game = Chess.game(Chess.standard)
        # Load board images
        self.piece_images = {
            "P": QPixmap("white_pawn.png"),
            "N": QPixmap("white_knight.png"),
            "B": QPixmap("white_bishop.png"),
            "R": QPixmap("white_rook.png"),
            "Q": QPixmap("white_queen.png"),
            "K": QPixmap("white_king.png"),
            "p": QPixmap("black_pawn.png"),
            "n": QPixmap("black_knight.png"),
            "b": QPixmap("black_bishop.png"),
            "r": QPixmap("black_rook.png"),
            "q": QPixmap("black_queen.png"),
            "k": QPixmap("black_king.png"),
        }
        for file in range(8):
            for rank in range(8):
                square = QLabel()
                square.setPixmap(white_square if (file + rank) % 2 == 0 else black_square)
                square.setScaledContents(True)  # Allow the QLabel to resize its content
                square.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                squares.addWidget(square, file, rank)
                notation = game.board[file][rank]
                if notation != '_':
                    piece = QLabel()
                    piece.setPixmap(self.piece_images[notation])
                    piece.setScaledContents(True)
                    piece.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    squares.addWidget(piece,file,rank)
        return board_container
    
    


