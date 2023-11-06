import copy

EMPTY, BLACK, WHITE = ".", "●", "○"
HUMAN, COMPUTER = "●", "○"

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)
VIC = 10000000  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SQUARES = [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

"""
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. flag to end game

"""


# The user decides who plays first
def whoIsFirst(s):
    global HUMAN, COMPUTER

    # loop until the user picks the starting collor that they would like (b/w)
    while True:
        i = input("What color would you like to be (b/w)? ")
        if i == "w":
            s[2] = HUMAN
            break
        if i == "b":
            s[2] = COMPUTER
            break

    return s


def isHumTurn(s):
    # Returns True iff it the human's turn to play
    return s[2] == HUMAN



# The HUMAN plays first (=BLACK)
def create():
    global HUMAN, COMPUTER
    board = [EMPTY] * 100
    for i in SQUARES:
        board[i] = EMPTY
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    HUMAN, COMPUTER = "●", "○"
    return [board, 0.00001, HUMAN, False]


def printState(s):
    rep = ""
    rep += "  %s\n" % " ".join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += "%d %s\n" % (row, " ".join(s[0][begin:end]))
    print(rep)

    if s[1] == VIC:
        print("Ha ha ha I won!")
    elif s[1] == LOSS:
        print("You did it!")
    elif s[1] == TIE:
        print("It's a TIE")


def inputMove(s):
    # Reads, enforces legality and executes the user's move.

    flag = True
    while flag:
        printState(s)
        move = int(
            input(
                "To make your move enter a two digits number, the first number is row and the second is column"
                "\n"
                "For example: if you want to choose the first row and the third column enter 13"
                "\n"
                "Enter your next move: "
            )
        )
        if isLegal(move, s) == False:
            print("Illegal move.")
        else:
            flag = False
            makeMove(move, s)


CORNERS = (11, 18, 88, 81)


def value(s):
    computerScore = sum(s[0][sq] == COMPUTER for sq in SQUARES)
    computerScore += sum(s[0][sq] == COMPUTER for sq in CORNERS) * 4
    humanScore = sum(s[0][sq] == HUMAN for sq in SQUARES)
    humanScore += sum(s[0][sq] == HUMAN for sq in CORNERS) * 4

    # give a point for each piece that the player has
    # add 4 more points for each corner piece the user has, as it is permanent
    # a benefit of keeping the scoring computationally cheap is you can go to a greater depth

    # 100% win rate against random (DEPTH = 5 [as given]) (200 trials)
    # https://piazza.com/class/lljdzwy1q461mc/post/43

    s[1] = computerScore - humanScore
    return s[1]


def isFinished(s):
    # Returns True if the game ended

    if not anyLegalMove(s):
        # anyLegalMove mutates s[3] to the return value of this function
        # whoWin's then sets the heuristic as either winning for a side
        # or a tie
        # this is useful for printing out the state
        s[1] = whoWin(s)

    return s[3]


def isLegal(move, s):
    hasbracket = lambda direction: findBracket(move, s, direction)
    return s[0][move] == EMPTY and any(map(hasbracket, DIRECTIONS))


# get a list of legal moves for the player
def legalMoves(s):
    return [sq for sq in SQUARES if isLegal(sq, s)]


# Is there any legal move for this player
def anyLegalMove(s):
    isAny = any(isLegal(sq, s) for sq in SQUARES)
    if not (isAny):
        s[3] = True
    return isAny


def makeFlips(move, s, direction):
    bracket = findBracket(move, s, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        s[0][square] = s[2]
        square += direction


def changePlayer(s):
    if s[2] == COMPUTER:
        s[2] = HUMAN
    else:
        s[2] = COMPUTER


def makeMove(move, s):
    s[0][move] = s[2]
    for d in DIRECTIONS:
        makeFlips(move, s, d)
    value(s)
    changePlayer(s)
    return s


def whoWin(s):
    computerScore = 0
    humanScore = 0
    for sq in SQUARES:
        piece = s[0][sq]
        if piece == COMPUTER:
            computerScore += 1
        elif piece == HUMAN:
            humanScore += 1
    if computerScore > humanScore:
        return VIC

    elif computerScore < humanScore:
        return LOSS

    elif computerScore == HUMAN:
        return TIE

    return 0.00001  # not 0 because TIE is 0


def isValid(move):
    return isinstance(move, int) and move in SQUARES


def findBracket(square, s, direction):
    bracket = square + direction
    if s[0][bracket] == s[2]:
        return None
    opp = BLACK if s[2] is WHITE else WHITE
    while s[0][bracket] == opp:
        bracket += direction
    return None if s[0][bracket] in (EMPTY) else bracket


def getNext(s):
    # returns a list of the next states of s
    ns = []
    for m in legalMoves(s):
        tmp = copy.deepcopy(s)
        makeMove(m, tmp)
        ns += [tmp]
    return ns
