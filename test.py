import string
import random as r
import time
def titleScreen():
    with open("titlescreen.txt") as file:
        for line in file:
            print(line,end="")
    print('-Enter anything to start')
    print('-Enter q to exit game')
    print('-Enter i to view instructions')
    x = input()
    if x == 'q':
        exit("Goodbye and see you again")
    elif x == 'i':
        print('Open(xy): Open the block (Explode if it is a mine)')
        print('Flag(xy F): Put a flag on that bqlock to mark it as a mine')
        print('Check(xy C): Clicking on a numbered square with the correct number of flags around it so others unknow block will be open(mine will be opened if you put the wrong flag)')
        titleScreen()
    elif x == "HoshinoAiIsTheBestIdol": #this is not expceted to be activated by player, only for devs
        return True
    else:
        return False
def choosemode():
    print("1. Classical\n2. Blind")
    while True:
        n = input("Choose gamemode (1,2):")
        if n == "1" or n == "2":
            return int(n)

def chooselevel():
    while True:
        print("1: Basic \n2: Advanced \n3: Expert \n4: Master \n5: Re:Master \n15: Pandora Paradoxxx (don't play this)")
        level = input("Choose Difficulty (1-5,15):")
        if level in ("1","2","3","4","5","15"):
            if level == "15":
                print("Are you sure? This is insanely hard that nearly half of them are bombs")
                if input("enter yes to start:") != "yes":
                    chooselevel()
            level = int(level)
            break
    return level

def createboard(size): #create empty board full of "X"
    board = []
    for i in range(size):
        board.append(["X"] * size)
    return board

def printboard(board):
    print("  ",end="")
    for i in range(len(board)):
        print(string.ascii_uppercase[i],end=" ")
    print()
    for i in range(len(board)):
        print(string.ascii_lowercase[i],end=" ")
        for j in range(len(board)):
            print(board[i][j],end=" ")
        print()

def playerinput(size, board, numboard):
    neighbors=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    while True:
        temp = input('Please enter coordinate(xy)(xy F)(xy C): ')
        
        if temp == "q":
            exit("Goodbye and see you again")
        if len(temp) <= 1:
            print('Invaild input')
        elif len(temp) == 2:
            if temp[0].isupper() or temp[1].islower():
                print("Invalid input\nPlease input small letter first then enter capital letter")
            elif temp[0] in string.ascii_lowercase[0:size] and temp[1] in string.ascii_uppercase[0:size]:
                coordinate = [string.ascii_lowercase.index(temp[0]),string.ascii_uppercase.index(temp[1]), 'N']
                i, j, k = coordinate
                if board[i][j] != 'X' or board[i][j] == 'F':
                    print('Invaild input')
                else:
                    break
            else:
                print('Invaild input')
        elif len(temp) == 4:
            if temp[0].isupper() or temp[1].islower():
                print("Invalid input\nPlease input small letter first then enter capital letter")
            elif temp[0] in string.ascii_lowercase[0:size] and temp[1] in string.ascii_uppercase[0:size] and temp[3] == 'F':
                coordinate = [string.ascii_lowercase.index(temp[0]),string.ascii_uppercase.index(temp[1]),'F']
                i, j, k = coordinate
                if board[i][j] == 'F':
                    break
                elif board[i][j] != 'X':
                    print('Invaild input')
                else:
                    break
            elif temp[0] in string.ascii_lowercase[0:size] and temp[1] in string.ascii_uppercase[0:size] and temp[3] == 'C':
                coordinate = [string.ascii_lowercase.index(temp[0]),string.ascii_uppercase.index(temp[1]),'C']
                i, j, k = coordinate
                count=0
                for pos in neighbors:
                    r,c=pos
                    try:
                        if board[i+r][j+c]=='F':
                            count+=1
                    except IndexError:
                        continue
                if board[i][j] not in [1,2,3,4,5,6,7,8]:
                    print('Invaild input')
                    
                elif count != numboard[i][j]:
                    print('Invaild input')                    
                else:
                    break
        
        else:
            print('Invaild input')
    return coordinate
        
def getboomposition(size,boom, initial_coordinate):
    boomlist = []
    i, j, k = initial_coordinate
    while len(boomlist) < boom:
        temp1 = [r.randint(0,size-1),r.randint(0,size-1)]
        if temp1 not in boomlist and temp1 != [i, j] :
            boomlist.append(temp1)
    return boomlist

def blocknum(boomlist,board,size): #List of numbur of boom close to that block(boom position is M)
    neighbors=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    numboard = []
    for i in board:
        numboard.append(list(i))
    for i in range(size):
        for ii in range(size):
            count=0
            if [i,ii] in boomlist:
                numboard[i][ii] = 'M'
                continue
            for j in neighbors:
                r,c=j
                try:
                    if [i+r,ii+c] in boomlist:
                        count+=1
                except IndexError:
                    pass 
            numboard[i][ii]=count
    return numboard

def boardchange(board, numboard, coordinate, boom):
    i, j, k = coordinate
    list0 = []
    neighbors=[(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)] 

    if k == 'F' and board[i][j] == 'F':
        board[i][j] = 'X'
    elif k == 'F':
        if stopFlag(numboard,board, boom):
            board[i][j] = 'F'
        else: print("Too many flags!")
    elif k == 'C':
        for pos in neighbors:
            r,c=pos
            try:
                if board[i+r][j+c]=='F':
                    continue
                elif board[i+r][j+c]=='X' and board[i+r][j+c]!='F':
                    newcoordinate=[i+r,j+c,'N']
                    boardchange(board,numboard,newcoordinate, boom)
            except IndexError:
                pass
    elif numboard[i][j] == 0:
        board[i][j] = numboard[i][j]
        list0 = [[i, j]]
        for l in list0:
            for pos in neighbors:
                r, c = pos
                x = abs(l[0]+r)
                y = abs(l[1]+c)
                try:
                    board[x][y] = numboard[x][y]
                    if numboard[x][y] == 0 and [x, y] not in list0:
                        list0.append([x, y])
                except IndexError:
                    continue
        list0.clear()
    elif numboard[i][j] == 'M':
        for i in range(len(numboard)):
            board[i] = numboard[i]
        
    else:       
        board[i][j] = numboard[i][j]

def blindmode(board):
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != "F":
                board[i][j] = "X"
    return board

def endScreen(win,timeused):
    if win:
        print('YOU WIN')
        print("You have finished the minesweeper in",round(timeused,2),"seconds. YAYYYYY!")
    else: 
        print("You Loose")
        rand = r.randint(1,4)
        deathspeech = {
            1: "Dr Dirk had died in the mines in Ukraine",
            2: "Dr Kit had his computer exploded and died",
            3: "Biden get boomed while playing with kids",
            4: "An assassin get boomed. He flew to the home of Hoshino Ai and stabbed her"
        }
        print(deathspeech[rand])
        print("pray them for 1 second")
        time.sleep(1)
    print('Enter anything to restart')
    print('Enter q to exit game')
    x = input()
    if x == 'q':                      
        exit("Goodbye and see you again")
    else:
        main()

def wincondition(board,numboard,mode,boom):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "X" and numboard[i][j] != "M" and mode == 1:
                return False
            if board[i][j] == "F" and numboard[i][j] == "M" and mode == 2:
                count += 1
    if mode == 1:
        return True
    if count == boom:
        return True
    else: return False

def stopFlag(boomlist,board, boom):
    countFlag = 0
    for i in board:
        for j in i:
            if j == 'F':
                countFlag += 1
    if countFlag >= boom:
        return False
    else:
        return True

def mineleft(boomlist,board):
    count=0
    for i in range(len(board)):
        for ii in range(len(board[0])):
            if board[i][ii]=='F':
                count+=1
    print('Mines left:',len(boomlist)-count)
def main():
    sizedict={1:10,2:15,3:20,4:26,5:26,15:26}
    boomdict={1:10,2:22,3:40,4:70,5:150,15:300}
    if titleScreen():
        size = int(input("enter size:"))
        boom = int(input("enter boom:"))
        mode = choosemode()
    else:
        mode = choosemode()
        difficulty = chooselevel()
        size = sizedict[difficulty]
        boom = boomdict[difficulty]
    board = createboard(size)
    printboard(board)
    numboard=[]
    coordinate = playerinput(size, board, numboard)
    time1 = time.time() 
    boomlist = getboomposition(size,boom, coordinate)
    numboard = blocknum(boomlist, board, size)
    while True: #wtf ar
        boardchange(board, numboard, coordinate,boom)
        if numboard == board:
            printboard(numboard)
            endScreen(False,1)
        if wincondition(board,numboard,mode,boom):
            printboard(board)
            timeused = time.time() - time1
            endScreen(True,timeused)
        mineleft(boomlist,board)
        printboard(board)
        coordinate = playerinput(size, board, numboard)
        if mode == 2 and coordinate[2] != "F": #blind mode
            board = blindmode(board)
        
main()
#board is the one display to player
#numboard is the hidden board

#seems fixed



