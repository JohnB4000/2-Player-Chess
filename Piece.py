import pygame

class Piece:
    def __init__(self, source):
        self.asset = pygame.image.load("Assets/" + source + ".png")
        self.asset = pygame.transform.scale(self.asset, (100, 100))

        self.possibleMove = pygame.image.load("Assets/possibleMove.png")
        self.possibleMove = pygame.transform.scale(self.possibleMove, (100, 100))

        self.colour = source[0]
        self.name = source[1]

        self.notMoved = True

        self.coords = [0, 0]
    
    def update(self, rank, file, isBoard):
        if isBoard:
            self.coords[0] = file * 100
            self.coords[1] = rank * 100
        else:
            self.coords[0] = file - 50
            self.coords[1] = rank - 50

    def show(self, screen):
        screen.blit(self.asset, (self.coords[0], self.coords[1]))

    def checkForEnemy(self, board, coords, whiteMove):
        if board[coords[0]][coords[1]] != None:
            if board[coords[0]][coords[1]].colour == ('b' if whiteMove else 'w'):
                return True
        return False

    def checkForCheck(self, pickedPiece, newCoords, board, whiteMove):
        temp = board[newCoords[0]][newCoords[1]]
        board[newCoords[0]][newCoords[1]] = pickedPiece
        rank = 0
        file = 0
        while rank <= 7:
            if board[rank][file] != None:
                if board[rank][file].name == 'k' and board[rank][file].colour == ('w' if whiteMove else 'b'):
                    inCheck = board[rank][file].checkIfInCheck([rank, file], board, whiteMove)
                    board[newCoords[0]][newCoords[1]] = temp
                    return inCheck
            if file == 7:
                file = 0
                rank += 1
            else:
                file += 1
        board[newCoords[0]][newCoords[1]] = temp
        return False




class Pawn(Piece):
    def __init__(self, source):
        super().__init__(source)
    
    def checkValidMove(self, oldCoords, newCoords, board, whiteMove, lastMove, lastPiece):
        if lastMove[0][0] == lastMove[1][0] - 2 and lastPiece == 'p':
            if newCoords[0] == lastMove[0][0] + 1 and newCoords[1] == lastMove[0][1] and oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] + 1:
                self.notMoved = False
                board[lastMove[1][0]][lastMove[1][1]] = None
                return True
            elif newCoords[0] == lastMove[0][0] + 1 and newCoords[1] == lastMove[0][1] and oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] - 1:
                self.notMoved = False
                board[lastMove[1][0]][lastMove[1][1]] = None
                return True
        if board[oldCoords[0] - 1][oldCoords[1]] == None:
            if oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif self.notMoved and board[newCoords[0]][newCoords[1]] == None and oldCoords[0] == newCoords[0] + 2 and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
        if self.checkForEnemy(board, newCoords, whiteMove) and (oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] + 1) or self.checkForEnemy(board, newCoords, whiteMove) and (oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] - 1):
            self.notMoved = False
            return True
        return False


    def showPossibleMoves(self, screen, pickedPiece, cameFrom, board, whiteMove, lastMove, lastPiece):
        if board[cameFrom[0] - 1][cameFrom[1]] == None:
            if not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, cameFrom[0] * 100 - 100))
            if self.notMoved and board[cameFrom[0] - 2][cameFrom[1]] == None and not self.checkForCheck(pickedPiece, [cameFrom[0] - 2, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, cameFrom[0] * 100 - 200))
        if cameFrom[0] >= 1:
            if board[cameFrom[0] - 1][cameFrom[1] - 1] != None:
                if board[cameFrom[0] - 1][cameFrom[1] - 1].colour == ('b' if whiteMove else 'w') and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1] - 1], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100 - 100))
        if cameFrom[1] <= 6:
            if board[cameFrom[0] - 1][cameFrom[1] + 1] != None:
                if board[cameFrom[0] - 1][cameFrom[1] + 1].colour == ('b' if whiteMove else 'w') and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1] + 1], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100 - 100))
        
        if lastMove[0][0] == lastMove[1][0] - 2 and lastPiece == 'p':
            if cameFrom[0] == lastMove[1][0] and cameFrom[1] == lastMove[1][1] + 1:
                screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100 - 100))
            if cameFrom[0] == lastMove[1][0] and cameFrom[1] == lastMove[1][1] - 1:
                screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100 - 100))




class Rook(Piece):
    def __init__(self, source):
        super().__init__(source)

    def checkValidMove(self, oldCoords, newCoords, board, whiteMove):
        rank = oldCoords[0] - 1
        pieceFound = False
        while rank >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][oldCoords[1]] != None:
                pieceFound = True
            rank -= 1

        pieceFound = False
        rank = oldCoords[0] + 1
        while rank <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][oldCoords[1]] != None:
                pieceFound = True
            rank += 1

        pieceFound = False
        file = oldCoords[1] - 1
        while file >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[oldCoords[0]][file] != None:
                pieceFound = True
            file -= 1

        pieceFound = False
        file = oldCoords[1] + 1
        while file <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[oldCoords[0]][file] != None:
                pieceFound = True
            file += 1
        return False


    def showPossibleMoves(self, screen, pickedPiece, cameFrom, board, whiteMove):
        rank = cameFrom[0] - 1
        pieceFound = False
        while rank >= 0 and not pieceFound:
            if self.checkForEnemy(board, [rank, cameFrom[1]], whiteMove) and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
                pieceFound = True
            elif board[rank][cameFrom[1]] == None and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
            elif board[rank][cameFrom[1]] != None:
                pieceFound = True
            rank -= 1

        rank = cameFrom[0] + 1
        pieceFound = False
        while rank <= 7 and not pieceFound:
            if self.checkForEnemy(board, [rank, cameFrom[1]], whiteMove) and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
                pieceFound = True
            elif board[rank][cameFrom[1]] == None and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
            elif board[rank][cameFrom[1]] != None:
                pieceFound = True
            rank += 1

        file = cameFrom[1] - 1
        pieceFound = False
        while file >= 0 and not pieceFound:
            if self.checkForEnemy(board, [cameFrom[0], file], whiteMove) and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
                pieceFound = True
            elif board[cameFrom[0]][file] == None and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
            elif board[cameFrom[0]][file] != None:
                pieceFound = True
            file -= 1
        
        file = cameFrom[1] + 1
        pieceFound = False
        while file <= 7 and not pieceFound:
            if self.checkForEnemy(board, [cameFrom[0], file], whiteMove) and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
                pieceFound = True
            elif board[cameFrom[0]][file] == None and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
            elif board[cameFrom[0]][file] != None:
                pieceFound = True
            file += 1




class Bishop(Piece):
    def __init__(self, source):
        super().__init__(source)
    
    def checkValidMove(self, oldCoords, newCoords, board, whiteMove):
        rank = oldCoords[0] - 1
        file = oldCoords[1] - 1
        pieceFound = False
        while rank >= 0 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file -= 1
        
        rank = oldCoords[0] + 1
        file = oldCoords[1] + 1
        pieceFound = False
        while rank <= 7 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file += 1
        
        rank = oldCoords[0] + 1
        file = oldCoords[1] - 1
        pieceFound = False
        while rank <= 7 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file -= 1

        rank = oldCoords[0] - 1
        file = oldCoords[1] + 1
        pieceFound = False
        while rank >= 0 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file += 1
        return False

    def showPossibleMoves(self, screen, pickedPiece, cameFrom, board, whiteMove):
        rank = cameFrom[0] - 1
        file = cameFrom[1] - 1
        pieceFound = False
        while rank >= 0 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file -= 1
        
        rank = cameFrom[0] + 1
        file = cameFrom[1] + 1
        pieceFound = False
        while rank <= 7 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file += 1
        
        rank = cameFrom[0] + 1
        file = cameFrom[1] - 1
        pieceFound = False
        while rank <= 7 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file -= 1
        
        rank = cameFrom[0] - 1
        file = cameFrom[1] + 1
        pieceFound = False
        while rank >= 0 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file += 1


        

class Knight(Piece):
    def __init__(self, source):
        super().__init__(source)
    
    def checkValidMove(self, oldCoords, newCoords, board, whiteMove):
        if oldCoords[0] == newCoords[0] + 2 and oldCoords[1] == newCoords[1] + 1 or oldCoords[0] == newCoords[0] + 2 and oldCoords[1] == newCoords[1] - 1 or oldCoords[0] == newCoords[0] - 2 and oldCoords[1] == newCoords[1] + 1 or oldCoords[0] == newCoords[0] - 2 and oldCoords[1] == newCoords[1] - 1 or oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] + 2 or oldCoords[0] == newCoords[0] - 1 and oldCoords[1] == newCoords[1] + 2 or oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] - 2 or oldCoords[0] == newCoords[0] - 1 and oldCoords[1] == newCoords[1] - 2:
            return True
        return False

    def showPossibleMoves(self, screen, pickedPiece, cameFrom, board, whiteMove):
        if cameFrom[0] >= 2:
            if cameFrom[1] <= 6:
                if (board[cameFrom[0] - 2][cameFrom[1] + 1] == None or self.checkForEnemy(board, [cameFrom[0] - 2, cameFrom[1] + 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 2, cameFrom[1] + 1], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100 - 200))
            if cameFrom[1] >= 1:
                if (board[cameFrom[0] - 2][cameFrom[1] - 1] == None or self.checkForEnemy(board, [cameFrom[0] - 2, cameFrom[1] - 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 2, cameFrom[1] - 1], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100 - 200))
        if cameFrom[0] <= 5:
            if cameFrom[1] <= 6:
                if (board[cameFrom[0] + 2][cameFrom[1] + 1] == None or self.checkForEnemy(board, [cameFrom[0] + 2, cameFrom[1] + 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 2, cameFrom[1] + 1], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100 + 200))
            if cameFrom[1] >= 1:
                if (board[cameFrom[0] + 2][cameFrom[1] - 1] == None or self.checkForEnemy(board, [cameFrom[0] + 2, cameFrom[1] - 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 2, cameFrom[1] - 1], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100 + 200))
        if cameFrom[1] >= 2:
            if cameFrom[0] <= 6:
                if (board[cameFrom[0] + 1][cameFrom[1] - 2] == None or self.checkForEnemy(board, [cameFrom[0] + 1, cameFrom[1] - 2], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 1, cameFrom[1] - 2], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 - 200, cameFrom[0] * 100 + 100))
            if cameFrom[0] >= 1:
                if (board[cameFrom[0] - 1][cameFrom[1] - 2] == None or self.checkForEnemy(board, [cameFrom[0] - 1, cameFrom[1] - 2], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1] - 2], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 - 200, cameFrom[0] * 100 - 100))
        if cameFrom[1] <= 5:
            if cameFrom[0] <= 6:
                if (board[cameFrom[0] + 1][cameFrom[1] + 2] == None or self.checkForEnemy(board, [cameFrom[0] + 1, cameFrom[1] + 2], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 1, cameFrom[1] + 2], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 + 200, cameFrom[0] * 100 + 100))
            if cameFrom[0] >= 1:
                if (board[cameFrom[0] - 1][cameFrom[1] + 2] == None or self.checkForEnemy(board, [cameFrom[0] - 1, cameFrom[1] + 2], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1] + 2], board, whiteMove):
                    screen.blit(self.possibleMove, (cameFrom[1] * 100 + 200, cameFrom[0] * 100 - 100))




class Queen(Piece):
    def __init__(self, source):
        super().__init__(source)
    
    def checkValidMove(self, oldCoords, newCoords, board, whiteMove):
        rank = oldCoords[0] - 1
        pieceFound = False
        while rank >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][oldCoords[1]] != None:
                pieceFound = True
            rank -= 1

        pieceFound = False
        rank = oldCoords[0] + 1
        while rank <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and oldCoords[1] == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][oldCoords[1]] != None:
                pieceFound = True
            rank += 1

        pieceFound = False
        file = oldCoords[1] - 1
        while file >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[oldCoords[0]][file] != None:
                pieceFound = True
            file -= 1

        pieceFound = False
        file = oldCoords[1] + 1
        while file <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif oldCoords[0] == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[oldCoords[0]][file] != None:
                pieceFound = True
            file += 1

        rank = oldCoords[0] - 1
        file = oldCoords[1] - 1
        pieceFound = False
        while rank >= 0 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file -= 1
        
        rank = oldCoords[0] + 1
        file = oldCoords[1] + 1
        pieceFound = False
        while rank <= 7 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file += 1
        
        rank = oldCoords[0] + 1
        file = oldCoords[1] - 1
        pieceFound = False
        while rank <= 7 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file -= 1

        rank = oldCoords[0] - 1
        file = oldCoords[1] + 1
        pieceFound = False
        while rank >= 0 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, newCoords, whiteMove) and rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif rank == newCoords[0] and file == newCoords[1]:
                self.notMoved = False
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file += 1
        return False
        
    def showPossibleMoves(self, screen, pickedPiece, cameFrom, board, whiteMove):
        rank = cameFrom[0] - 1
        pieceFound = False
        while rank >= 0 and not pieceFound:
            if self.checkForEnemy(board, [rank, cameFrom[1]], whiteMove) and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
                pieceFound = True
            elif board[rank][cameFrom[1]] == None and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
            elif board[rank][cameFrom[1]] != None:
                pieceFound = True
            rank -= 1

        rank = cameFrom[0] + 1
        pieceFound = False
        while rank <= 7 and not pieceFound:
            if self.checkForEnemy(board, [rank, cameFrom[1]], whiteMove) and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
                pieceFound = True
            elif board[rank][cameFrom[1]] == None and not self.checkForCheck(pickedPiece, [rank, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, rank * 100))
            elif board[rank][cameFrom[1]] != None:
                pieceFound = True
            rank += 1

        file = cameFrom[1] - 1
        pieceFound = False
        while file >= 0 and not pieceFound:
            if self.checkForEnemy(board, [cameFrom[0], file], whiteMove) and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
                pieceFound = True
            elif board[cameFrom[0]][file] == None and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
            elif board[cameFrom[0]][file] != None:
                pieceFound = True
            file -= 1
        
        file = cameFrom[1] + 1
        pieceFound = False
        while file <= 7 and not pieceFound:
            if self.checkForEnemy(board, [cameFrom[0], file], whiteMove) and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
                pieceFound = True
            elif board[cameFrom[0]][file] == None and not self.checkForCheck(pickedPiece, [cameFrom[0], file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, cameFrom[0] * 100))
            elif board[cameFrom[0]][file] != None:
                pieceFound = True
            file += 1
    
        rank = cameFrom[0] - 1
        file = cameFrom[1] - 1
        pieceFound = False
        while rank >= 0 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file -= 1
        
        rank = cameFrom[0] + 1
        file = cameFrom[1] + 1
        pieceFound = False
        while rank <= 7 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file += 1
        
        rank = cameFrom[0] + 1
        file = cameFrom[1] - 1
        pieceFound = False
        while rank <= 7 and file >= 0 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file -= 1
        
        rank = cameFrom[0] - 1
        file = cameFrom[1] + 1
        pieceFound = False
        while rank >= 0 and file <= 7 and not pieceFound:
            if self.checkForEnemy(board, [rank, file], whiteMove) and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
                pieceFound = True
            elif board[rank][file] == None and not self.checkForCheck(pickedPiece, [rank, file], board, whiteMove):
                screen.blit(self.possibleMove, (file * 100, rank * 100))
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file += 1




class King(Piece):
    def __init__(self, source):
        super().__init__(source)
    
    def checkValidMove(self, oldCoords, newCoords, board, whiteMove):
        if oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] + 1 or oldCoords[0] == newCoords[0] - 1 and oldCoords[1] == newCoords[1] - 1 or oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] - 1 or oldCoords[0] == newCoords[0] - 1 and oldCoords[1] == newCoords[1] + 1 or oldCoords[0] == newCoords[0] + 1 and oldCoords[1] == newCoords[1] or oldCoords[0] == newCoords[0] - 1 and oldCoords[1] == newCoords[1] or oldCoords[0] == newCoords[0] and oldCoords[1] == newCoords[1] + 1 or oldCoords[0] == newCoords[0] and oldCoords[1] == newCoords[1] - 1:
            self.notMoved = False
            return True

        if not self.checkIfInCheck(newCoords, board, whiteMove):
            if whiteMove:
                if self.notMoved and newCoords[0] == 7 and newCoords[1] == 6 and board[7][7] != None and board[7][5] == None:
                    if board[7][7].notMoved:
                        self.notMoved = False
                        board[7][7].notMoved = False
                        board[7][5] = board[7][7]
                        board[7][7] = None
                        return True
                if self.notMoved and newCoords[0] == 7 and newCoords[1] == 2 and board[7][0] != None and board[7][1] == None and board[7][3] == None:
                    if board[7][0].notMoved:
                        self.notMoved = False
                        board[7][0].notMoved = False
                        board[7][3] = board[7][0]
                        board[7][0] = None
                        return True
            else:
                if self.notMoved and newCoords[0] == 7 and newCoords[1] == 5 and board[7][7] != None and board[7][6] == None and board[7][4] == None:
                    if board[7][7].notMoved and board[7][7].name == 'r':
                        self.notMoved = False
                        board[7][7].notMoved = False
                        board[7][4] = board[7][7]
                        board[7][7] = None
                        return True
                if self.notMoved and newCoords[0] == 7 and newCoords[1] == 1 and board[7][0] != None and board[7][2] == None:
                    if board[7][0].notMoved and board[7][0].name == 'r':
                        self.notMoved = False
                        board[7][0].notMoved = False
                        board[7][2] = board[7][0]
                        board[7][0] = None
                        return True
        return False
    
    def showPossibleMoves(self, screen, pickedPiece, cameFrom, board, whiteMove):
        if cameFrom[0] >= 1:
            if (board[cameFrom[0] - 1][cameFrom[1]] == None or self.checkForEnemy(board, [cameFrom[0] - 1, cameFrom[1]], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, cameFrom[0] * 100 - 100))
        if cameFrom[0] <= 6:
            if (board[cameFrom[0] + 1][cameFrom[1]] == None or self.checkForEnemy(board, [cameFrom[0] + 1, cameFrom[1]], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 1, cameFrom[1]], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100, cameFrom[0] * 100 + 100))
        if cameFrom[1] >= 1:
            if (board[cameFrom[0]][cameFrom[1] - 1] == None or self.checkForEnemy(board, [cameFrom[0], cameFrom[1] - 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0], cameFrom[1] - 1], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100))
        if cameFrom[1] <= 6:
            if (board[cameFrom[0]][cameFrom[1] + 1] == None or self.checkForEnemy(board, [cameFrom[0], cameFrom[1] + 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0], cameFrom[1] + 1], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100))

        if cameFrom[0] >= 1 and cameFrom[1] >= 1:
            if (board[cameFrom[0] - 1][cameFrom[1] - 1] == None or self.checkForEnemy(board, [cameFrom[0] - 1, cameFrom[1] - 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1] - 1], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100 - 100))
        if cameFrom[0] <= 6 and cameFrom[1] <= 6:
            if (board[cameFrom[0] + 1][cameFrom[1] + 1] == None or self.checkForEnemy(board, [cameFrom[0] + 1, cameFrom[1] + 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 1, cameFrom[1] + 1], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100 + 100))
        if cameFrom[0] <= 6 and cameFrom[1] >= 1:
            if (board[cameFrom[0] + 1][cameFrom[1] - 1] == None or self.checkForEnemy(board, [cameFrom[0] + 1, cameFrom[1] - 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] + 1, cameFrom[1] - 1], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100 - 100, cameFrom[0] * 100 + 100))
        if cameFrom[0] >= 1 and cameFrom[1] <= 6:
            if (board[cameFrom[0] - 1][cameFrom[1] + 1] == None or self.checkForEnemy(board, [cameFrom[0] - 1, cameFrom[1] + 1], whiteMove)) and not self.checkForCheck(pickedPiece, [cameFrom[0] - 1, cameFrom[1] + 1], board, whiteMove):
                screen.blit(self.possibleMove, (cameFrom[1] * 100 + 100, cameFrom[0] * 100 - 100))
        
        if not self.checkIfInCheck(cameFrom, board, whiteMove):
            if whiteMove:
                if self.notMoved and board[7][7] != None and board[7][5] == None and board[7][6] == None:
                    if board[7][0].notMoved and board[7][7].name == 'r':
                        screen.blit(self.possibleMove, (cameFrom[1] * 100 + 200, cameFrom[0] * 100))
                
                if self.notMoved and board[7][0] != None and board[7][1] == None and board[7][2] == None and board[7][3] == None:
                    if board[7][0].notMoved and board[7][0].name == 'r':
                        screen.blit(self.possibleMove, (cameFrom[1] * 100 - 200, cameFrom[0] * 100))
            else:
                if self.notMoved and board[7][7] != None and board[7][6] == None and board[7][5] == None and board[7][4] == None:
                    if board[7][7].notMoved and board[7][7].name == 'r':
                        screen.blit(self.possibleMove, (cameFrom[1] * 100 + 200, cameFrom[0] * 100))
                
                if self.notMoved and board[7][0] != None and board[7][1] == None and board[7][2] == None:
                    if board[7][0].notMoved and board[7][0].name == 'r':
                        screen.blit(self.possibleMove, (cameFrom[1] * 100 - 200, cameFrom[0] * 100))

    
    def checkIfInCheck(self, newCoords, board, whiteMove):
        rank = newCoords[0] - 1
        pieceFound = False
        while rank >= 0 and not pieceFound:
            if self.checkForRookQueen(board, [rank, newCoords[1]], whiteMove):
                return True
            elif board[rank][newCoords[1]] != None:
                pieceFound = True
            rank -= 1

        rank = newCoords[0] + 1
        pieceFound = False
        while rank <= 7 and not pieceFound:
            if self.checkForRookQueen(board, [rank, newCoords[1]], whiteMove):
                return True
            elif board[rank][newCoords[1]] != None:
                pieceFound = True
            rank += 1

        file = newCoords[1] - 1
        pieceFound = False
        while file >= 0 and not pieceFound:
            if self.checkForRookQueen(board, [newCoords[0], file], whiteMove):
                return True
            elif board[newCoords[0]][file] != None:
                pieceFound = True
            file -= 1
        
        file = newCoords[1] + 1
        pieceFound = False
        while file <= 7 and not pieceFound:
            if self.checkForRookQueen(board, [newCoords[0], file], whiteMove):
                return True
            elif board[newCoords[0]][file] != None:
                pieceFound = True
            file += 1

        rank = newCoords[0] - 1
        file = newCoords[1] - 1
        pieceFound = False
        while rank >= 0 and file >= 0 and not pieceFound:
            if self.checkForBishopQueen(board, [rank, file], whiteMove):
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file -= 1

        rank = newCoords[0] + 1
        file = newCoords[1] - 1
        pieceFound = False
        while rank <= 7 and file >= 0 and not pieceFound:
            if self.checkForBishopQueen(board, [rank, file], whiteMove):
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file -= 1

        rank = newCoords[0] - 1
        file = newCoords[1] + 1
        pieceFound = False
        while rank >= 0 and file <= 7 and not pieceFound:
            if self.checkForBishopQueen(board, [rank, file], whiteMove):
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank -= 1
            file += 1

        rank = newCoords[0] + 1
        file = newCoords[1] + 1
        pieceFound = False
        while rank <= 7 and file <= 7 and not pieceFound:
            if self.checkForBishopQueen(board, [rank, file], whiteMove):
                return True
            elif board[rank][file] != None:
                pieceFound = True
            rank += 1
            file += 1

        if newCoords[0] >= 1 and newCoords[1] >= 1:
            if self.checkForPawn(board, [newCoords[0] - 1, newCoords[1] - 1], whiteMove) or self.checkForKing(board, [newCoords[0] - 1, newCoords[1] - 1], whiteMove):
                return True

        if newCoords[0] >= 1 and newCoords[1] <= 6:
            if self.checkForPawn(board, [newCoords[0] - 1, newCoords[1] + 1], whiteMove) or self.checkForKing(board, [newCoords[0] - 1, newCoords[1] + 1], whiteMove):
                return True

        if newCoords[0] >= 1:
            if self.checkForKing(board, [newCoords[0] - 1, newCoords[1]], whiteMove):
                return True

        if newCoords[0] <= 6:
            if self.checkForKing(board, [newCoords[0] + 1, newCoords[1]], whiteMove):
                return True

        if newCoords[1] >= 1:
            if self.checkForKing(board, [newCoords[0], newCoords[1] - 1], whiteMove):
                return True

        if newCoords[1] <= 6:
            if self.checkForKing(board, [newCoords[0], newCoords[1] + 1], whiteMove):
                return True

        if newCoords[0] <= 6 and newCoords[1] >= 1:
            if self.checkForKing(board, [newCoords[0] + 1, newCoords[1] - 1], whiteMove):
                return True

        if newCoords[0] <= 6 and newCoords[1] <= 6:
            if self.checkForKing(board, [newCoords[0] + 1, newCoords[1] + 1], whiteMove):
                return True


        if newCoords[0] >= 2:
            if newCoords[1] <= 6:
                if self.checkForKnight(board, [newCoords[0] - 2, newCoords[1] + 1], whiteMove):
                    return True
            if newCoords[1] >= 1:
                if self.checkForKnight(board, [newCoords[0] - 2, newCoords[1] - 1], whiteMove):
                    return True
        if newCoords[0] <= 5:
            if newCoords[1] <= 6:
                if self.checkForKnight(board, [newCoords[0] + 2, newCoords[1] + 1], whiteMove):
                    return True
            if newCoords[1] >= 1:
                if self.checkForKnight(board, [newCoords[0] + 2, newCoords[1] - 1], whiteMove):
                    return True
        if newCoords[1] >= 2:
            if newCoords[0] <= 6:
                if self.checkForKnight(board, [newCoords[0] + 1, newCoords[1] - 2], whiteMove):
                    return True
            if newCoords[0] >= 1:
                if self.checkForKnight(board, [newCoords[0] - 1, newCoords[1] - 2], whiteMove):
                    return True
        if newCoords[1] <= 5:
            if newCoords[0] <= 6:
                if self.checkForKnight(board, [newCoords[0] + 1, newCoords[1] + 2], whiteMove):
                    return True
            if newCoords[0] >= 1:
                if self.checkForKnight(board, [newCoords[0] - 1, newCoords[1] + 2], whiteMove):
                    return True
        return False

    
    def checkForRookQueen(self, board, coords, whiteMove):
        if board[coords[0]][coords[1]] != None:
            if board[coords[0]][coords[1]].colour == ('b' if whiteMove else 'w'):
                if board[coords[0]][coords[1]].name == 'r' or board[coords[0]][coords[1]].name == 'q':
                    return True
        return False

    def checkForBishopQueen(self, board, coords, whiteMove):
        if board[coords[0]][coords[1]] != None:
            if board[coords[0]][coords[1]].colour == ('b' if whiteMove else 'w'):
                if board[coords[0]][coords[1]].name == 'b' or board[coords[0]][coords[1]].name == 'q':
                    return True
        return False

    def checkForPawn(self, board, coords, whiteMove):
        if board[coords[0]][coords[1]] != None:
            if board[coords[0]][coords[1]].colour == ('b' if whiteMove else 'w'):
                if board[coords[0]][coords[1]].name == 'p':
                    return True
        return False

    def checkForKing(self, board, coords, whiteMove):
        if board[coords[0]][coords[1]] != None:
            if board[coords[0]][coords[1]].colour == ('b' if whiteMove else 'w'):
                if board[coords[0]][coords[1]].name == 'k':
                    return True
        return False

    def checkForKnight(self, board, coords, whiteMove):
        if board[coords[0]][coords[1]] != None:
            if board[coords[0]][coords[1]].colour == ('b' if whiteMove else 'w'):
                if board[coords[0]][coords[1]].name == 'n':
                    return True
        return False