"""
Éste archivo se encargará de cargar con los datos, llevar cuenta de los movientos válidos, así como permitirlos.
"""

class gameState ():
    def __init__ (self):
        self.board = [
            ["bL", "bN", "bS", "bQ", "bK", "bQ", "bS", "bN", "bL"],
            ["--", "bR", "--", "--", "--", "--", "--", "bB", "--"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["--", "wB", "--", "--", "--", "--", "--", "wR", "--"],
            ["wL", "wN", "wS", "wQ", "wK", "wQ", "wS", "wN", "wL"]
        ]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 
                              'L': self.getLancerMoves, 'N': self.getKnightMoves, 
                              'B': self.getBishopMoves, 'S': self.getSilverMoves, 
                              'Q': self.getGoldenMoves, 'K': self.getKingMoves, 
                              'と': self.getGoldenMoves, '今': self.getGoldenMoves, 
                              '仝': self.getGoldenMoves, '銀': self.getGoldenMoves, 
                              '馬': self.getDoragonMoves, '竜': self.getDragonMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (8, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.staleMate = False

    """
    Permite hacer los movimientos que son ya porcesados en la clase Move (No sirve para los movimientos especiales como el enroque, las promociones de peones o las capturas al paso de los mismos).
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Registra en el log los movientos, permitiendo deshacerlos luego.
        self.whiteToMove = not self.whiteToMove #Cambia el turno.

        #Actualización de ambos reyes, el rey negro y el blanco.
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #Promosión de las piezas.
        if move.pawnPromotion == True: #Peón.

            if move.promotion == True: #Para cuando se tiene la opción de promocionar la pieza.
                volund = input('¿Quiere promocionar este peón? y/n ')
                if volund == 'y':
                    print("Peón promocionado.")
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'と'

            if move.promoForce == True: #Cuando la promoción es obligatoria.
                print("Peón promocionado.")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'と'
        
        if move.lancerPromotion == True: #Lancero.
            
            if move.promotion == True: #Para cuando se tiene la opción de promocionar la pieza.
                volund = input('¿Quiere promocionar este lancero? y/n ')
                if volund == 'y':
                    print("Lancero promocionado.")
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '仝'

            if move.promoForce == True: #Cuando la promoción es obligatoria.
                print("Lancero promocionado.")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '仝'
            
        if move.knightPromotion == True: #Caballo.

            if move.promotion == True:
                volund = input('¿Quiere promocionar este caballo? y/n ')
                if volund == 'y':
                    print("Caballo promocionado.")
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '今'

            if move.promoForce == True:
                print("Caballo promocionado.")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '今'
            
        if move.silverPromotion == True: #General de plata.

            if move.promotion == True:
                volund = input('¿Quiere promocionar este general de plata? y/n ')
                if volund == 'y':
                    print("General de plata promocionado.")
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '銀'

            """if move.promoForce == True:
                print("Caballo promocionado.")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '銀'"""

        if move.bishopPromotion == True: #Alfíl.

            if move.promotion == True:
                volund = input('¿Quiere promocionar este alfin? y/n ')
                if volund == 'y':
                    print("Alfíl promocionado.")
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '馬'

            """if move.promoForce == True:
                print("Alfíl promocionado.")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '馬'"""

        if move.rookPromotion == True: #Torre.

            if move.promotion == True:
                volund = input('¿Quiere promocionar esta torre? y/n ')
                if volund == 'y':
                    print("Torre promocionada.")
                    self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '竜'

            """if move.promoForce == True:
                print("Torre promocionada.")
                self.board[move.endRow][move.endCol] = move.pieceMoved[0] + '竜'"""

    """
    Permite regresar un movimiento.
    """
    def undoMove(self):
        if len(self.moveLog) != 0: #Se asegura de que se haya hecho algún movimiento con anterioridad.
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #Actualización de ambos reyes, el rey negro y el blanco.
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            self.checkMate = False
            self.staleMate = False

    """
    Chequeo de los movientos considerando los jaques.
    """
    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1: #Al haber un jaque, se bloquea el jaque o se mueve el rey.
                moves = self.getAllPossibleMoves()
                #Para garantizar que se pueda poner una pieza cuyo moviento pueda bloquear un jaque.
                check = self.checks[0] #Revisión de la info del jaque.
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol] #La pieza que genera el jaque.
                validSquares = [] #Las casillas libres para el moviento del rey.
                #En caso de que sea el caballo, el rey se mueve o se captura al caballo.
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i) 
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol: #Cuando una pieza termina clavada.
                            break
                #Se cuentan todos los movientos que protegen al rey de jaque o donde el rey pueda moverse para librarse.
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else: #Jaque por partida doble, a fuerza se debe mover el rey.
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        return moves

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
            
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)): #Filas.
            d = directions[j]
            possiblePin = () #Se reinician las piezas clavadas.
            for i in range(1, 8): #Columnas.
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        if possiblePin == (): #Cuando hay una pieza que está clavada.
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else: #Cuando hay dos piezas.
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                            ((i == 1 or 0 <= j <= 3) and type == '竜') or\
                            (4 <= j <= 7 and type == 'B') or \
                            ((i == 1 or 4 <= j <= 7) and type == '馬') or\
                            (i == 1 and type == 'P' and ((enemyColor == 'w' and 2 <= j <= 2) or (enemyColor == 'b' and 0 <= j <= 0))) or \
                            (i == 1 and type == 'S' and ((enemyColor == 'w' and ((6 <= j <= 7) or (2 <= j <= 2) or (4 <= j <= 5))) or \
                                                        (enemyColor == 'b' and ((6 <= j <= 7) or (0 <= j <= 0) or (4 <= j <= 5))))) or \
                            (i == 1 and type == 'K'):
                            if possiblePin == (): #El jaque al haber espacio libre.
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else: #Se clava una pieza cuando está en medio de un jaque.
                                pins.append(possiblePin)
                                break
                        else: #En caso de no haber de jaque o amenaza de uno.
                            break
                else: #Fuera de límites.
                    break
        
        #Los movientos según el bando en turno.            
        if self.whiteToMove: #Cuando sea el turno de las negras.
            moveAmount = -1
            goldenDirections = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, 1), (-1, -1))
        else: #Cuando sea el turno de las blancas.
            moveAmount = 1
            goldenDirections = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (1, 1))

        #Jaques del general dorado..
        allyColor = "w" if self.whiteToMove else "b"
        for m in goldenDirections:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 9 and 0 <= endCol < 9:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and (endPiece[1] == 'Q' or endPiece[1] == 'と' or endPiece[1] == '仝' or\
                                                  endPiece[1] == '今' or endPiece[1] == '銀'): #Cuando el general dorado, o cualquier pieza ascendida menos el alfil y la torre, ataca al rey.
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        #Jaques del caballo.
        knightMoves = (((2 * moveAmount), 1), ((2 * moveAmount), -1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 9 and 0 <= endCol < 9:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N': #Cuando el caballo ataca al rey.
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks
    
    """
    Chequeo de todos los movimientos posibles.
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #Filas.
            for c in range(len(self.board[r])): #Columnas.
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): #El bando que tenga el turno.
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) #Llama la función correspondiente al moviento de la pieza en turno. Por ejemplo: si la pieza en turno es el caballo (N), llamará la función que fue asociada al ID.
        return moves

    """
    Los movimientos de las piezas, peón, torre, lancero, caballo, alfín, general dorado, general plateado y rey, en ese orden.
    """
    def getPawnMoves(self, r, c, moves):
        """Esto lo que hace es verificar el estado de la pieza y si detecta que por 
        encima de ella hay un posible jaque al rey, entonces la bloquea."""
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            backRow = 0
            enemyColor = 'b'
            oppField = [1, 2]
        else:
            moveAmount = 1
            backRow = 8
            enemyColor = 'w'
            oppField = [7, 6]

        pawnPromotion = False
        promotion = False
        promoForce = False

        if self.board[r + moveAmount][c] == '--': #Movimientos de una casilla.
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:
                    pawnPromotion = True
                    promoForce = True
                if r + moveAmount == oppField[0] or r + moveAmount == oppField[1]:
                    pawnPromotion = True
                    promotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion = pawnPromotion, promotion = promotion, promoForce = promoForce))
    
        if not piecePinned or pinDirection == (moveAmount, -1): #Captura según su moviento.
            if self.board[r + moveAmount][c][0] == enemyColor:
                if r + moveAmount == backRow:
                    pawnPromotion = True
                    promoForce = True
                if r + moveAmount == oppField[0] or r + moveAmount == oppField[1]:
                    pawnPromotion = True
                    promotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion = pawnPromotion, promotion = promotion, promoForce = promoForce))

    def getRookMoves(self, r, c, moves):
        """Esto lo que hace es verificar el estado de la pieza y si detecta que por 
        encima de ella hay un posible jaque al rey, entonces la bloquea."""
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True                
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break
            
        #Los movientos naturales de la pieza.
        if self.whiteToMove: #Cuando sea el turno de las negras.
            backRow = 0
            oppField = [1, 2]
        else: #Cuando sea el turno de las blancas.
            backRow = 8
            oppField = [7, 6]

        rookPromotion = True
        promotion = True
        forcePromo = True

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 9):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            if endRow != backRow: #En caso de que la pieza esté en una fila que no sea la del contrincante.
                                rookPromotion = False
                                promotion = False
                            else: #En caso de que la pieza esté en la fila del contrincante.
                                rookPromotion = True
                                promotion = True
                            if endRow == oppField[0] or endRow == oppField[1]:
                                rookPromotion = True
                                promotion = True
                            moves.append(Move((r, c), (endRow, endCol), self.board, rookPromotion = rookPromotion, promotion = promotion))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            if endRow != backRow:
                                rookPromotion = False
                                promotion = False
                            else:
                                rookPromotion = True
                                promotion = True
                            if endRow == oppField[0] or endRow == oppField[1]:
                                rookPromotion = True
                                promotion = True
                            moves.append(Move((r, c), (endRow, endCol), self.board, rookPromotion = rookPromotion, promotion = promotion))
                            break
                        else: #Evitar el fuego aliado.
                            break
                else: #Fuera del tablero.
                    break
    
    def getLancerMoves(self, r, c, moves):
        """Esto lo que hace es verificar el estado de la pieza y si detecta que por 
        encima de ella hay un posible jaque al rey, entonces la bloquea."""
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True                
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break
        #Los movientos naturales de la pieza.
        if self.whiteToMove:
            moveAmount = -1
            backRow = 0
            oppField = [1, 2]
        else:
            moveAmount = 1
            backRow = 8
            oppField = [7, 6]
        
        lancerPromotion = False
        promotion = False
        promoForce = False
        
        directions = ((moveAmount, 0), (0, 0))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 9):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            if endRow + moveAmount == backRow:
                                lancerPromotion = True
                                promoForce = True
                            if endRow == oppField[0] or endRow == oppField[1]:
                                lancerPromotion = True
                                promotion = True
                            moves.append(Move((r, c), (endRow, endCol), self.board, lancerPromotion = lancerPromotion, promotion = promotion, promoForce = promoForce))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            if endRow + moveAmount == backRow:
                                lancerPromotion = True
                                promoForce = True
                            if endRow == oppField[0] or endRow == oppField[1]:
                                lancerPromotion = True
                                promotion = True
                            moves.append(Move((r, c), (endRow, endCol), self.board, lancerPromotion = lancerPromotion, promotion = promotion, promoForce = promoForce))
                            break
                        else: #Evitar el fuego aliado.
                            break
                else: #Fuera del tablero.
                    break

    def getKnightMoves(self, r, c, moves):
        """Esto lo que hace es verificar el estado de la pieza y si detecta que por 
        encima de ella hay un posible jaque al rey, entonces la bloquea."""
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove: #Cuando sea el turno de las negras.
            moveAmount = -1
            backRow = 0
            oppField = [1, 2]
        else: #Cuando sea el turno de las blancas.
            moveAmount = 1
            backRow = 8
            oppField = [7, 6]

        knightPromotion = False
        promotion = False
        promoForce = False
        knightMoves = (((2 * moveAmount), 1), ((2 * moveAmount), -1))

        #Los movientos naturales de la pieza.
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 9 and 0 <= endCol < 9:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #Tanto para el desplazamiento como para la captura.
                        if endRow == backRow or endRow == oppField[0]:
                            knightPromotion = True
                            promoForce = True
                        if endRow == oppField[1]:
                            knightPromotion = True
                            promotion = True
                        moves.append(Move((r, c), (endRow, endCol), self.board, knightPromotion = knightPromotion, promotion = promotion, promoForce = promoForce))

    def getBishopMoves(self, r, c, moves):
        """Esto lo que hace es verificar el estado de la pieza y si detecta que por 
        encima de ella hay un posible jaque al rey, entonces la bloquea."""
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True                
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        #Los movientos naturales de la pieza.

        if self.whiteToMove: #Cuando sea el turno de las negras.
            backRow = 0
            oppField = [1, 2]
        else: #Cuando sea el turno de las blancas.
            backRow = 8
            oppField = [7, 6]

        bishopPromotion = False
        promotion = False
        promoForce = False

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 9):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            if endRow == backRow:
                                bishopPromotion = True
                                promoForce = True
                            if endRow == oppField[0] or endRow == oppField[1]:
                                bishopPromotion = True
                                promotion = True
                            moves.append(Move((r, c), (endRow, endCol), self.board, bishopPromotion = bishopPromotion, promotion = promotion, promoForce = promoForce))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            if endRow == backRow:
                                bishopPromotion = True
                                promoForce = True
                            if endRow == oppField:
                                bishopPromotion = True
                                promotion = True
                            moves.append(Move((r, c), (endRow, endCol), self.board, bishopPromotion = bishopPromotion, promotion = promotion, promoForce = promoForce))
                            break
                        else: #Evitar el fuego aliado.
                            break
                    else: #Fuera del tablero.
                        break
    
    def getDoragonMoves(self, r, c, moves):
        #Alfíl promocionado.
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True                
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 9):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #Evitar el fuego aliado.
                            break
                    else: #Fuera del tablero.
                        break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 2):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #Evitar el fuego aliado.
                            break
                else: #Fuera del tablero.
                    break

    def getDragonMoves(self, r, c, moves):
        #Torre promocionada.
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True                
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 9):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #Evitar el fuego aliado.
                            break
                else: #Fuera del tablero.
                    break

        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 2):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #Evitar el fuego aliado.
                            break
                    else: #Fuera del tablero.
                        break

    def getGoldenMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True                
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
            
        if self.whiteToMove: #Cuando sea el turno de las negras.
            directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, 1), (-1, -1))
        else: #Cuando sea el turno de las blancas.
            directions = ((1, 0), (0, 1), (-1, 0), (0, -1), (1, -1), (1, 1))

        #Los movientos naturales de la pieza.
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 2):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 9 and 0 <= endCol < 9: #Dentro del tablero.
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]): #Evita mover la pieza en caso de que esté clavada.
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--": #Espacio libre y válido.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor: #Captura legal.
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else: #Evitar el fuego aliado.
                            break
                    else:
                        break
                else: #Fuera del tablero.
                    break
        
    def getSilverMoves(self, r, c, moves):
        """Esto lo que hace es verificar el estado de la pieza y si detecta que por 
        encima de ella hay un posible jaque al rey, entonces la bloquea."""
        piecePinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove: #Cuando sea el turno de las negras.
            directions = ((1, 1), (-1, 1), (1, -1), (-1, -1), (-1, 0))
            backRow = 0
            oppField = [1, 2]
        else: #Cuando sea el turno de las blancas.
            directions = ((-1, -1), (1, -1), (-1, 1), (1, 1), (1, 0))
            backRow = 8
            oppField = [7, 6]

        silverPromotion = False
        promotion = False

        #Los movientos naturales de la pieza.
        allyColor = "w" if self.whiteToMove else "b"
        for m in directions:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 9 and 0 <= endCol < 9:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor: #Tanto para el desplazamiento como para la captura.
                        if endRow == backRow:
                            silverPromotion = True
                            promotion = True
                        if endRow == oppField[0] or endRow == oppField[1]:
                            silverPromotion = True
                            promotion = True
                        moves.append(Move((r, c), (endRow, endCol), self.board, silverPromotion = silverPromotion, promotion = promotion))
        
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"
        for m in range(8):
            endRow = r + rowMoves[m]
            endCol = c + colMoves[m]
            if 0 <= endRow < 9 and 0 <= endCol < 9:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #Tanto para el desplazamiento como para la captura.
                    if allyColor == 'w': #Actualización de las coordenas del rey blanco.
                        self.whiteKingLocation = (endRow, endCol)
                    else: #Actualización de las coordenas del rey negro.
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks  = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

"""
Procesado de los permisos de los movientos de desplazamiento como especiales. También genera las coordenadas.
"""
class Move():
    ranksToRows = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"9": 0, "8": 1, "7": 2, "6": 3, "5": 4, "4": 5, "3": 6, "2": 7, "1": 8}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, pawnPromotion = False, lancerPromotion = False, knightPromotion = False, silverPromotion = False, bishopPromotion = False, rookPromotion = False, promotion = False, promoForce = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.pawnPromotion = pawnPromotion
        self.lancerPromotion = lancerPromotion
        self.knightPromotion = knightPromotion
        self.silverPromotion = silverPromotion
        self.bishopPromotion = bishopPromotion
        self.rookPromotion = rookPromotion
        self.promotion = promotion
        self.promoForce = promoForce
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.pieceMoved + ' ' +(self.getRankFile(self.startRow, self.startCol) + ', ' + self.getRankFile(self.endRow, self.endCol))

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
