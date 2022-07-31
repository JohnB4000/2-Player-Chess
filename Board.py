import Piece, pygame

class Board:
    def __init__(self):
        self.board = [[None for file in range(8)] for rank in range(8)]
        self.createPieces()

        self.pickedPiece = None
        self.cameFrom = [0, 0]

        self.whiteMove = True

        self.lastMove = [[0, 0], [0, 0]]
        self.lastPiece = ''

        self.whiteBackground = pygame.image.load("Assets/WhiteBackgroundBoard.png")
        self.whiteBackground = pygame.transform.scale(self.whiteBackground, (800, 800))

        self.blackBackground = pygame.image.load("Assets/BlackBackgroundBoard.png")
        self.blackBackground = pygame.transform.scale(self.blackBackground, (800, 800))
    

    def update(self):
        clickedRank, clickedFile = self.findClickedSquare()
        if self.pickedPiece == None:
            if self.board[clickedRank][clickedFile] != None:
                if self.board[clickedRank][clickedFile].colour == ('w' if self.whiteMove else 'b'):
                    self.pickedPiece = self.board[clickedRank][clickedFile]
                    self.board[clickedRank][clickedFile] = None
                    self.cameFrom = [clickedRank, clickedFile]
        elif self.pickedPiece != None:
            if self.board[clickedRank][clickedFile] == None or self.board[clickedRank][clickedFile].colour == ('b' if self.whiteMove else 'w'):
                if self.cameFrom[0] == clickedRank and self.cameFrom[1] == clickedFile:
                    self.board[clickedRank][clickedFile] = self.pickedPiece
                    self.pickedPiece = None
                else:
                    validMove = self.pickedPiece.checkValidMove(self.cameFrom, [clickedRank, clickedFile], self.board, self.whiteMove, self.lastMove, self.lastPiece) if self.pickedPiece.name == 'p' else self.pickedPiece.checkValidMove(self.cameFrom, [clickedRank, clickedFile], self.board, self.whiteMove)
                    moveMade = True
                    if validMove and self.pickedPiece != None:
                        if self.pickedPiece.name == 'p' and clickedRank == 0:
                            self.pickedPiece = Piece.Queen('wq' if self.whiteMove else 'bq')

                        temp = self.board[clickedRank][clickedFile]
                        self.board[clickedRank][clickedFile] = self.pickedPiece
                    
                        inCheck = self.checkForCheck([clickedRank, clickedFile])
                        if inCheck:
                            self.board[clickedRank][clickedFile] = temp
                            moveMade = False
                        
                        if moveMade:
                            self.lastMove = [[7 - self.cameFrom[0], 7 - self.cameFrom[1]], [7 - clickedRank, 7 - clickedFile]]
                            self.lastPiece = self.pickedPiece.name
                            self.pickedPiece = None
                            self.movePlayed()
            

    def show(self, screen):
        screen.blit(self.whiteBackground, (0, 0))
        for rank in range(8):
            for file in range(8):
                if self.board[rank][file] != None:
                    self.board[rank][file].update(rank, file, True)
                    self.board[rank][file].show(screen)

        if self.pickedPiece != None:
            mouse = pygame.mouse.get_pos()
            self.pickedPiece.showPossibleMoves(screen, self.pickedPiece, self.cameFrom, self.board, self.whiteMove, self.lastMove, self.lastPiece) if self.pickedPiece.name == 'p' else self.pickedPiece.showPossibleMoves(screen, self.pickedPiece, self.cameFrom, self.board, self.whiteMove)
            
            self.pickedPiece.update(mouse[1], mouse[0], False)
            self.pickedPiece.show(screen)


    def createPieces(self):
        self.board[0][0] = Piece.Rook('br')
        self.board[0][1] = Piece.Knight('bn')
        self.board[0][2] = Piece.Bishop('bb')
        self.board[0][3] = Piece.Queen('bq')
        self.board[0][4] = Piece.King('bk')
        self.board[0][5] = Piece.Bishop('bb')
        self.board[0][6] = Piece.Knight('bn')
        self.board[0][7] = Piece.Rook('br')

        for counter in range(8):
            self.board[1][counter] = Piece.Pawn('bp')

        for counter in range(8):
            self.board[6][counter] = Piece.Pawn('wp')

        self.board[7][0] = Piece.Rook('wr')
        self.board[7][1] = Piece.Knight('wn')
        self.board[7][2] = Piece.Bishop('wb')
        self.board[7][3] = Piece.Queen('wq')
        self.board[7][4] = Piece.King('wk')
        self.board[7][5] = Piece.Bishop('wb')
        self.board[7][6] = Piece.Knight('wn')
        self.board[7][7] = Piece.Rook('wr')


    def findClickedSquare(self):
        mouse = pygame.mouse.get_pos()
        for rank in range(8):
            for file in range(8):
                if mouse[0] >= file * 100 and mouse[0] <= (file * 100) + 100 and mouse[1] >= rank * 100 and mouse[1] <= (rank * 100) + 100:
                    return rank, file
    
    
    def movePlayed(self):
        self.whiteMove = False if self.whiteMove else True

        for rank in range(8):
            self.board[rank].reverse()
        self.board.reverse()

    def checkForCheck(self, newCoords):
        rank = 0
        file = 0
        while rank <= 7:
            if self.board[rank][file] != None:
                if self.board[rank][file].name == 'k' and self.board[rank][file].colour == ('w' if self.whiteMove else 'b'):
                    return self.board[rank][file].checkIfInCheck([rank, file], self.board, self.whiteMove)
            if file == 7:
                file = 0
                rank += 1
            else:
                file += 1
        if self.pickedPiece.name == 'k' and self.pickedPiece.colour == ('w' if self.whiteMove else 'b'):
                return self.pickedPiece.checkIfInCheck(newCoords, self.board, self.whiteMove)
        return False

# Can castle through check