from Tile import Tile
import copy
changed = False
changeNums = set({})
changeRows = set({})
changeCols = set({})
changeBox = set({})
tiles = []
for row in range(9):
    tiles.append([])
    for col in range(9):
        tiles[row].append(Tile())
board = [ [0, 0, 0,     0, 0, 0,      0, 0, 0],
          [0, 0, 0,     0, 0, 0,      0, 0, 0],
          [0, 0, 0,     0, 0, 0,      0, 0, 0],

          [0, 0, 0,     0, 0, 0,      0, 0, 0],
          [0, 0, 0,     0, 0, 0,      0, 0, 0],
          [0, 0, 0,     0, 0, 0,      0, 0, 0],

          [0, 0, 0,     0, 0, 0,      0, 0, 0],
          [0, 0, 0,     0, 0, 0,      0, 0, 0],
          [0, 0, 0,     0, 0, 0,      0, 0, 0]]
def printGrid(grid):
    for r in range(9):
        for c in range(9):
            if c % 3 == 2:
                print(grid[r][c], end="    ")
            else:
                print(grid[r][c], end=" ")
        if r % 3 == 2:
            print()
        print()

# changes each result list
def change(num, r, c):
    global changed
    changed = True
    changeNums.add(num)
    changeRows.add(r)
    changeCols.add(c)
    changeBox.add((int(r / 3), int(c / 3)))

# places num
def place(r, c, num,grid):
    if len(changeNums) < 9:
        for item in grid[r][c].posNums:
            changeNums.add(item)
    grid[r][c].number = num
    grid[r][c].posNums.clear()
    change(num, r, c)
    for i in range(9):
        grid[r][i].posNums.discard(num)
    for i in range(9):
        grid[i][c].posNums.discard(num)
    r = r - (r % 3)
    c = c - (c % 3)
    for i in range(3):
        for j in range(3):
            grid[r + i][c + j].posNums.discard(num)

# checks to see if there's only one option for a tile
def checkOne(grid):
    for r in range(9):
        for c in range(9):
            if len(grid[r][c].posNums) == 1:
                curNum = grid[r][c].posNums.pop()
                place(r, c, curNum,grid)

# checks to see if there's only one option for where num could go in each r,c,b
def onlyOption(resNums, resRows, resCols, resBox,grid):
    for num in range(1, 10):
        if num not in resNums:
            continue
        for r in range(9):
            if r not in resRows:
                continue
            appearances = 0
            col = -1
            for c in range(9):
                if num in grid[r][c].posNums:
                    appearances += 1
                    if appearances > 1:
                        break
                    col = c
            if appearances == 1:
                place(r, col, num,grid)
        for c in range(9):
            if c not in resCols:
                continue
            appearances = 0
            row = -1
            for r in range(9):
                if num in grid[r][c].posNums:
                    appearances += 1
                    if appearances > 1:
                        break
                    row = r
            if appearances == 1:
                place(row, c, num,grid)
        for bigR in range(3):
            for bigC in range(3):
                if (bigR, bigC) not in resBox:
                    continue
                appearances = 0
                col = -1
                row = -1
                for r in range(3):
                    if appearances > 1:
                        break
                    for c in range(3):
                        if num in grid[bigR * 3 + r][bigC * 3 + c].posNums:
                            appearances += 1
                            row = bigR * 3 + r
                            col = bigC * 3 + c
                if appearances == 1:
                    place(row, col, num,grid)

# finds and updates hidden 2s and 3s, doesn't work on boxes
def hiddenTwoThrees(resRows, resCols,grid):
    for r in range(9):
        if r not in resRows:
            continue
        colsList = [0,[],[],[],[],[],[],[],[],[]]
        for c in range(9):
            for num in grid[r][c].posNums:
                colsList[num].append(c)
        twoList = []
        threeList = []
        for i in range(1,len(colsList)):
            if len(colsList[i]) == 2:
                twoList.append(i)
            elif len(colsList[i]) == 3:
                threeList.append(i)
        i=0
        while i<len(twoList):
            if len(twoList) < 2:
                break
            j=i+1
            while j<len(twoList):
                if colsList[twoList[i]]==colsList[twoList[j]]:
                    discardList=[]
                    for num in grid[r][colsList[twoList[i]][0]].posNums:
                        if num==twoList[i] or num==twoList[j]:
                            continue
                        discardList.append(num)
                        change(num,r,colsList[twoList[i]][0])
                    for item in discardList:
                        grid[r][colsList[twoList[i]][0]].posNums.discard(item)
                    discardList = []
                    for num in grid[r][colsList[twoList[i]][1]].posNums:
                        if num == twoList[i] or num == twoList[j]:
                            continue
                        discardList.append(num)
                        change(num, r, colsList[twoList[i]][1])
                    for item in discardList:
                        grid[r][colsList[twoList[i]][1]].posNums.discard(item)
                    twoList.pop(j)
                    twoList.pop(i)
                    i-=1
                    break
                j+=1
            i+=1
        i=0
        while i < len(threeList):
            if len(threeList) < 3:
                break
            j=i+1
            while j <len(threeList):
                done=False
                if colsList[threeList[i]] == colsList[threeList[j]]:
                    k=j+1
                    while k < len(threeList):
                        if colsList[threeList[i]] == colsList[threeList[k]]:
                            discardList=[]
                            for num in grid[r][colsList[threeList[i]][0]].posNums:
                                if num == threeList[i] or num == threeList[j] or num==threeList[k]:
                                    continue
                                discardList.append(num)
                                change(num, r, colsList[threeList[i]][0])
                            for item in discardList:
                                grid[r][colsList[threeList[i]][0]].posNums.discard(item)
                            discardList.clear()
                            for num in grid[r][colsList[threeList[i]][1]].posNums:
                                if num == threeList[i] or num == threeList[j] or num==threeList[k]:
                                    continue
                                discardList.append(num)
                                change(num, r, colsList[threeList[i]][1])
                            for item in discardList:
                                grid[r][colsList[threeList[i]][1]].posNums.discard(item)
                            discardList.clear()
                            for num in grid[r][colsList[threeList[i]][2]].posNums:
                                if num == threeList[i] or num == threeList[j] or num==threeList[k]:
                                    continue
                                discardList.append(num)
                                change(num, r, colsList[threeList[i]][2])
                            for item in discardList:
                                grid[r][colsList[threeList[i]][2]].posNums.discard(item)
                            threeList.pop(k)
                            threeList.pop(j)
                            threeList.pop(i)
                            i-=1
                            done=True
                            break
                        k+=1
                if done:
                    break
                j+=1
            i+=1
    for c in range(9):
        if c not in resCols:
            continue
        rowsList = [0, [], [], [], [], [], [], [], [], []]
        for r in range(9):
            for num in grid[r][c].posNums:
                rowsList[num].append(r)
        twoList = []
        threeList = []
        for i in range(1, len(rowsList)):
            if len(rowsList[i]) == 2:
                twoList.append(i)
            elif len(rowsList[i]) == 3:
                threeList.append(i)
        i = 0
        while i < len(twoList):
            if len(twoList) < 2:
                break
            j = i + 1
            while j < len(twoList):
                if rowsList[twoList[i]] == rowsList[twoList[j]]:
                    discardList = []
                    for num in grid[rowsList[twoList[i]][0]][c].posNums:
                        if num == twoList[i] or num == twoList[j]:
                            continue
                        discardList.append(num)
                        change(num, rowsList[twoList[i]][0], c)
                    for item in discardList:
                        grid[rowsList[twoList[i]][0]][c].posNums.discard(item)
                    discardList = []
                    for num in grid[rowsList[twoList[i]][1]][c].posNums:
                        if num == twoList[i] or num == twoList[j]:
                            continue
                        discardList.append(num)
                        change(num, rowsList[twoList[i]][1],c)
                    for item in discardList:
                        grid[rowsList[twoList[i]][1]][c].posNums.discard(item)
                    twoList.pop(j)
                    twoList.pop(i)
                    i -= 1
                    break
                j += 1
            i += 1
        i = 0
        while i < len(threeList):
            if len(threeList) < 3:
                break
            j = i + 1
            while j < len(threeList):
                done = False
                if rowsList[threeList[i]] == rowsList[threeList[j]]:
                    k = j + 1
                    while k < len(threeList):
                        if rowsList[threeList[i]] == rowsList[threeList[k]]:
                            discardList = []
                            for num in grid[rowsList[threeList[i]][0]][c].posNums:
                                if num == threeList[i] or num == threeList[j] or num == threeList[k]:
                                    continue
                                discardList.append(num)
                                change(num, rowsList[threeList[i]][0],c)
                            for item in discardList:
                                grid[rowsList[threeList[i]][0]][c].posNums.discard(item)
                            discardList.clear()
                            for num in grid[rowsList[threeList[i]][1]][c].posNums:
                                if num == threeList[i] or num == threeList[j] or num == threeList[k]:
                                    continue
                                discardList.append(num)
                                change(num, rowsList[threeList[i]][1], c)
                            for item in discardList:
                                grid[rowsList[threeList[i]][1]][c].posNums.discard(item)
                            discardList.clear()
                            for num in grid[rowsList[threeList[i]][2]][c].posNums:
                                if num == threeList[i] or num == threeList[j] or num == threeList[k]:
                                    continue
                                discardList.append(num)
                                change(num, rowsList[threeList[i]][2],c)
                            for item in discardList:
                                grid[rowsList[threeList[i]][2]][c].posNums.discard(item)
                            threeList.pop(k)
                            threeList.pop(j)
                            threeList.pop(i)
                            i -= 1
                            done = True
                            break
                        k += 1
                if done:
                    break
                j += 1
            i += 1

# checks to see if there's x options in x tiles in each r,c,b
def xOptions(resRows, resCols, resBox,grid):
    for r in range(9):
        if r not in resRows:
            continue
        colList = []
        for c in range(9):
            length = len(grid[r][c].posNums)
            if 1 < length < 8:
                colList.append(c)
        while len(colList) > 1:
            sameList = []
            i = 1
            while i < len(colList):
                if grid[r][colList[i]].posNums == grid[r][colList[0]].posNums:
                    sameList.append(colList[i])
                    colList.pop(i)
                    i -= 1
                i += 1
            sameList.append(colList[0])
            if len(sameList) == len(grid[r][colList[0]].posNums):
                for c in range(9):
                    if c not in sameList:
                        for j in grid[r][sameList[0]].posNums:
                            if j in grid[r][c].posNums:
                                change(j, r, c)
                                grid[r][c].posNums.discard(j)
            colList.pop(0)
    for c in range(9):
        if c not in resCols:
            continue
        rowList = []
        for r in range(9):
            length = len(grid[r][c].posNums)
            if 1 < length < 8:
                rowList.append(r)
        while len(rowList) > 1:
            sameList = []
            i = 1
            while i < len(rowList):
                if grid[rowList[i]][c].posNums == grid[rowList[0]][c].posNums:
                    sameList.append(rowList[i])
                    rowList.pop(i)
                    i -= 1
                i += 1
            sameList.append(rowList[0])
            if len(sameList) == len(grid[rowList[0]][c].posNums):
                for r in range(9):
                    if r not in sameList:
                        for j in grid[rowList[0]][c].posNums:
                            if j in grid[r][c].posNums:
                                change(j, r, c)
                                grid[r][c].posNums.discard(j)
            rowList.pop(0)
    for bigR in range(3):
        for bigC in range(3):
            if (bigR, bigC) not in resBox:
                continue
            tupleList = []
            for r in range(3):
                for c in range(3):
                    length = len(grid[bigR * 3 + r][bigC * 3 + c].posNums)
                    if 1 < length < 8:
                        tupleList.append((bigR * 3 + r, bigC * 3 + c))
            while len(tupleList) > 1:
                sameList = []
                i = 1
                while i < len(tupleList):
                    if grid[tupleList[i][0]][tupleList[i][1]].posNums == grid[tupleList[0][0]][tupleList[0][1]].posNums:
                        sameList.append(tupleList[i])
                        tupleList.pop(i)
                        i -= 1
                    i += 1
                sameList.append(tupleList[0])
                if len(sameList) == len(grid[tupleList[0][0]][tupleList[0][1]].posNums):
                    for r in range(3):
                        for c in range(3):
                            if (bigR * 3 + r, bigC * 3 + c) not in sameList:
                                for j in grid[tupleList[0][0]][tupleList[0][1]].posNums:
                                    if j in grid[bigR * 3 + r][bigC * 3 + c].posNums:
                                        change(j, r, c)
                                        grid[bigR * 3 + r][bigC * 3 + c].posNums.discard(j)
                tupleList.pop(0)

#checks to see if grid could still have a valid answer
def isValid(grid):
    for r in range(9):
        for c in range(9):
            if len(grid[r][c].posNums)==0 and grid[r][c].number is None:
                return False
    return True

def isSolved(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c].number is None:
                return False
    return True

def recursiveStrats(r,c,num,grid):
    global changed
    place(r,c,num,grid)
    while True:
        if not isValid(grid):
            return attemptNum, attemptR, attemptC
        if isSolved(grid):
            return grid
        lChanged = changed
        changed = False
        if lChanged:
            lChangeNums = changeNums.copy()
            lChangeRows = changeRows.copy()
            lChangeCols = changeCols.copy()
            lChangeBox = changeBox.copy()
            changeNums.clear()
            changeRows.clear()
            changeCols.clear()
            changeBox.clear()
            checkOne(grid)
            onlyOption(lChangeNums, lChangeRows, lChangeCols, lChangeBox, grid)
            hiddenTwoThrees(lChangeRows, lChangeCols, grid)
            xOptions(lChangeRows, lChangeCols, lChangeBox, grid)
        else:
            copyGrid = copy.deepcopy(grid)
            rstop = False
            rattemptR = None
            rattemptC = None
            rattemptNum = None
            for r in range(9):
                for c in range(9):
                    if grid[r][c].number is None:
                        rattemptR = r
                        rattemptC = c
                        rattemptNum = grid[r][c].posNums.pop()
                        rstop = True
                        break
                if rstop:
                    break
            result = recursiveStrats(rattemptR,rattemptC,rattemptNum,copyGrid)
            if type(result) is list:
                return result
            else:
                change(result[0], result[1], result[2])
                grid[result[1]][result[2]].posNums.discard(result[0])

for row in range(9):
    for col in range(9):
        if board[row][col]!=0:
            place(row,col,board[row][col],tiles)
while True:
    if isSolved(tiles):
        printGrid(tiles)
        break
    lastChanged=changed
    changed=False
    if lastChanged:
        lastChangeNums = changeNums.copy()
        lastChangeRows = changeRows.copy()
        lastChangeCols = changeCols.copy()
        lastChangeBox = changeBox.copy()
        changeNums.clear()
        changeRows.clear()
        changeCols.clear()
        changeBox.clear()
        checkOne(tiles)
        onlyOption(lastChangeNums,lastChangeRows,lastChangeCols,lastChangeBox,tiles)
        hiddenTwoThrees(lastChangeRows, lastChangeCols, tiles)
        xOptions(lastChangeRows, lastChangeCols, lastChangeBox, tiles)
    else:
        stop = False
        attemptR = None
        attemptC = None
        attemptNum = None
        for r in range(9):
            for c in range(9):
                if tiles[r][c].number is None:
                    attemptR = r
                    attemptC = c
                    attemptNum = tiles[r][c].posNums.pop()
                    stop = True
                    break
            if stop:
                break
        copyTiles=copy.deepcopy(tiles)
        result=recursiveStrats(attemptR,attemptC,attemptNum,copyTiles)
        if type(result) is list:
            tiles=result
            break
        elif type(result) is tuple:
            change(result[0], result[1], result[2])
printGrid(tiles)