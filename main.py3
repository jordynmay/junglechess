# Dictionaries to convert between file letter and integer
fileToInd = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6}
fileToLetter = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g"}

rankToInd = {1:8, 2:7, 3:6, 4:5, 5:4, 6:3, 7:2, 8:1, 9:0}
indToRank = {0:9, 1:8, 2:7, 3:6, 4:5, 5:4, 6:3, 7:2, 8:1}

# Dictionaries to convert between piece character and integer
pieceToNum = {"r":1, "c":2, "d":3, "w":4, "p":5, "t":6, "l":7, "e":8,
              "R":-1, "C":-2, "D":-3, "W":-4, "P":-5, "T":-6, "L":-7, "E":-8}
numToPiece = {1:"r", 2:"c", 3:"d", 4:"w", 5:"p", 6:"t", 7:"l", 8:"e",
              -1:"R", -2:"C", -3:"D", -4:"W", -5:"P", -6:"T", -7:"L", -8:"E",
              0:"-"}

# Pieces can move up, down, left, and right
offsets = [(-1,0), (1,0), (0,-1), (0,1)]

water = [(3,1), (3,2), (3,4), (3,5), (4,1), (4,2), (4,4), (4,5),
    (5,1), (5,2), (5,4), (5,5)]

den = [(0,3), (8,3)]

trap = [(0,2), (0,4), (1,3), (8,2), (8,4), (7,3)]

class move:
    def __init__(self, starti=0, startj=0, endi=0, endj=0, pieceMoved=0, pieceCaptured=0):
        self.starti = starti
        self.startj = startj
        self.endi = endi
        self.endj = endj
        self.pieceMoved = pieceMoved
        self.pieceCaptured = pieceCaptured
    
    def printMove(self):
        # First, print the move in UCI format
        print(self.getUCIFromMove())

        # Second, print other potentially relevant information
        print("Piece moved: ",numToPiece[self.pieceMoved])
        if(self.pieceCaptured != 0):
            captured = numToPiece[self.pieceCaptured]
        else:
            captured = "N/A"
        print("Piece captured: ",captured)

    def printMoveUCI(self):
        print(self.getUCIFromMove())
    
    def getUCIFromMove(self):
        startFile = str(fileToLetter[self.startj])
        startRank = str(indToRank[self.starti])
        endFile = str(fileToLetter[self.endj])
        endRank = str(indToRank[self.endi])
        startUCIstr = startFile+startRank
        endUCIstr = endFile+endRank
        return startUCIstr+endUCIstr
    
    def clone(self, original):
        self.starti = original.starti
        self.startj = original.startj
        self.endi = original.endi
        self.endj = original.endj
        self.pieceMoved = original.pieceMoved
        self.pieceCaptured = original.pieceCaptured

class gameInstance:
    def __init__(self, board=[], activeColor="b", halfmove=0, fullmove=1):
        self.board = board
        self.activeColor = activeColor
        self.halfmove = halfmove
        self.fullmove = fullmove

    def printInfo(self):
        print("Board: ")
        self.printBoard()
        print("Active color: ",self.activeColor)
        print("Halfmove: ",self.halfmove)
        print("Fullmove: ",self.fullmove)

    def clone(self, original):
        self.board = [[] for l in original.board]
        for i in range(len(original.board)):
            self.board[i] = [c for c in original.board[i]]
        self.activeColor = original.activeColor
        self.halfmove = original.halfmove
        self.fullmove = original.fullmove

    def printBoard(self):
        havePrinted = False
        for i in range(9):
            for j in range(7):
                if(self.board[i][j] == 0):
                    if((i,j) in water):
                        print("\u283F"," ",end="")
                        havePrinted = True
                    elif((i,j) in den):
                        # \u00D7 is x
                        # \u3141 is a rectangle
                        print("\u00D7"," ",end="")
                        havePrinted = True
                    elif((i,j) in trap):
                        print("#"," ",end="")
                        havePrinted = True
                if(not havePrinted):
                    print(numToPiece[self.board[i][j]]," ",end="")
                havePrinted = False
            print("\n")

def printMoveList(moveList):
    tempList = []
    for item in moveList:
        # Individually convert moves into UCI strings
        UCI_str = item.getUCIFromMove()
        tempList.append(UCI_str)
    # Print the list of UCI strings
    print(tempList)

def getUCIList(moveList):
    UCIlist = []
    for item in moveList:
        UCIlist.append(item.getUCIFromMove())
    return UCIlist

def initBoard():
    board = []
    tempRow = []
    for j in range(7):
        tempRow.append(0)
    for i in range(9):
        board.append(tempRow)
    # print(board)
    # for row in board:
    #     for cell in row:
    #         print(cell," ",end="")
    #     print()
    return board

def fillBoard(board, board_str):
    rows = board_str.split("/")
    i = 0
    j = 0
    tempRow = []
    for row in rows:
        for char in row:
            if(char.isalpha()):
                #board[i][j] = pieceToNum[char]
                tempRow.append(pieceToNum[char])
                j = j+1
            elif(char.isnumeric()):
                #print("appending ",char," spaces to board")
                # j = j + int(char)
                for k in range(int(char)):
                    #board[i][j] = 0
                    tempRow.append(0)
                    j = j+1
        board[i] = tempRow
        i = i+1
        j = 0
        tempRow = []
    # for i in range(len(board)):
    #     print(board[i])
    return board
        
def getStateFromFen(fen):
    fen_list = fen.split()
    # Initialize and fill our board
    board = initBoard()

    board = fillBoard(board,fen_list[0])
    # for i in range(len(board)):
    #     print(board[i])

    # Extract other fen information
    color = fen_list[1]
    halfmove = int(fen_list[2])
    fullmove = int(fen_list[3])

    # Create game instance object
    gameState = gameInstance(board,color,halfmove,fullmove)
    #print("----------------------------------------")
    #print("BOARD FROM FEN STRING...")
    #gameState.printInfo()
    #print("----------------------------------------")
    return gameState

def outOfBounds(i,j):
    if(i<0 or j<0 or i>8 or j>6):
        return True

def cellOccupiedByOpponent(gameState, i, j):
    color = gameState.activeColor
    if(outOfBounds(i,j)):
        return False
    if(color == "b" and gameState.board[i][j] > 0):
        return True
    if(color == "r" and gameState.board[i][j] < 0):
        return True
    return False

def canCapture(gameState, starti, startj, endi, endj):
    startRank = abs(gameState.board[starti][startj])
    endRank = abs(gameState.board[endi][endj])
    if(startRank >= endRank):
        # Elephants cannot capture rats
        if(startRank == 8 and endRank == 1):
            return False
        # Otherwise, pieces can capture anything of lower rank
        return True
    # Rats can capture elephants
    if(startRank == 1 and endRank == 8):
        return True
    if((endi,endj) in trap):
        return True
    return False

def jumpOverWater(starti, startj, endi, endj):
    newEndi = endi
    newEndj = endj
    # If trying to move horizontally
    if(starti == endi):
        if(startj > endj):
            newEndj -= 2
        else:
            newEndj += 2
    # Else trying to move vertically
    elif(startj == endj):
        # Jump over water in either direction
        if(starti > endi):
            newEndi -= 3
        else:
            newEndi += 3
    return [newEndi, newEndj]

def generalMoves(gameState, i, j, offsets, isContinuous):
    moveList = []
    tempi = i
    tempj = j
    tempMove = move()
    tempMove.starti = i
    tempMove.startj = j
    tempMove.pieceMoved = gameState.board[i][j]

    for offset in offsets:
        tempi = i
        tempj = j
        done = False
        while(not done):
            tempi = tempi + offset[0]
            tempj = tempj + offset[1]
            if(outOfBounds(tempi,tempj)):
                done = True # Out of bounds so stop
            # If we are trying to move into water
            elif((tempi,tempj) in water):
                # If piece trying to move into water is NOT a rat
                if(abs(gameState.board[i][j]) != 1):
                    # If piece is NOT a lion or tiger
                    if(abs(gameState.board[i][j]) != 6 and abs(gameState.board[i][j]) != 7):
                        done = True
                    # Otherwise, lions and tigers can jump over water
                    else:
                        newCoords = jumpOverWater(i,j,tempi,tempj)
                        tempi = newCoords[0]
                        tempj = newCoords[1]
            if(not done):
                tempMove.endi = tempi
                tempMove.endj = tempj
                tempMove.pieceCaptured = gameState.board[tempi][tempj]

                # If new index is occupied
                if(gameState.board[tempi][tempj] != 0):
                    # If cell contains an opponent's piece
                    if(cellOccupiedByOpponent(gameState,tempi,tempj)):
                        # If we can capture
                        if(canCapture(gameState,i,j,tempi,tempj)):
                            done = True
                            appendMove = move()
                            appendMove.clone(tempMove)
                            moveList.append(appendMove)
                    # Else, cell contains your own piece
                    else:
                        done = True
                else:
                    appendMove = move()
                    appendMove.clone(tempMove)
                    moveList.append(appendMove)
            if(not isContinuous):
                done = True
    return moveList

def getAllMoves(gameState):
    color = gameState.activeColor
    tempMoveList = []
    possibleMove = False
    legalMoves = []

    if(color == "b"):
        colorFactor = -1
    else:
        colorFactor = 1
    for i in range(9):
        for j in range(7):
            possibleMove = False

            # # If piece in cell is our own rat
            # if(gameState.board[i][j]*colorFactor == 1):
            #     tempMoveList = generalMoves(gameState,i,j,offsets,False)
            # If piece in cell is our own piece
            if(gameState.board[i][j]*colorFactor > 0):
                tempMoveList = generalMoves(gameState,i,j,offsets,False)
                possibleMove = True

            if(possibleMove):
                legalMoves.extend(tempMoveList)
    # print("\nLegal moves: ")
    # printMoveList(legalMoves)
    return legalMoves

def performGeneralMove(gameState, move):
    starti = move.starti
    startj = move.startj
    endi = move.endi
    endj = move.endj
    gameState.board[endi][endj] = gameState.board[starti][startj]
    gameState.board[starti][startj] = 0
    if(gameState.activeColor == "b"):
        gameState.activeColor = "r"
    else:
        gameState.activeColor = "b"
        gameState.fullmove += 1
    if(move.pieceCaptured != 0):
        gameState.halfmove = 0
    else:
        gameState.halfmove += 1

def main():
    fen = "l5t/1d3c1/r1p1w1e/7/7/7/E1W1P1R/1C3D1/T5L b 0 1"
    #fen = "l5t/1d3c1/r1p1w1e/7/7/7/E1W1PLR/1C3D1/T6 b 0 1"
    #fen = "l1T3t/1dp2c1/r3w1e/7/7/7/E1W1PLR/1C3D1/7 r 0 1"

    continueMoving = True
    gameBoard = getStateFromFen(fen)
    gameBoard.printInfo()

    ## a3a5 (pieces cannot move more than one space generally),,
    ## c3c4 (only rats can move into water, so wolf cannot)
    # a3a4, a7a6 (move E forward, move R down)
    # f2e2, a6b6 (move D sideways, R can move into water)
    # g1f1, g7g6 (L moving sideways, E moving down)
    # f1f2, g6g5 (L moving forward, E moving down)
    # f2f3, g5g4 (L moving forward, E moving down)
    # f3f7, g9g8 (L jumps over water, T down / E cannot capture R)
    # g3g4 (R captures E)

    while(continueMoving):
        moveList = getAllMoves(gameBoard)
        print("\nMove list: ")
        printMoveList(moveList)
        UCIlist = getUCIList(moveList)
        choice = input("Pick a move from the list: ")
        try:
            moveInd = UCIlist.index(choice)
        except ValueError:
            moveInd = -1

        if(moveInd != -1):
            print("\nPerforming move ",moveList[moveInd].getUCIFromMove())

            performGeneralMove(gameBoard,moveList[moveInd])
            #gameBoard.printInfo()
            gameBoard.printBoard()
            keepMoving = input("Do you want to make another move? (yes/no): ")
            if(keepMoving != "yes" and keepMoving != "y"):
                continueMoving = False
        else:
            continueMoving = False
            print("\n\nThat is not a valid move",end="")
        print("\n-----------------------------------------")


if __name__ == "__main__":
    main()