def adjacency(rows,cols):
    """ returns an (NxM) x (NxM) matrix of zeros except ones for
    king's-move adjacent cells

    Most of the difficulty here is on the edges
    """
    
    assert cols > 1
    assert rows > 1
    dim = rows * cols
    mat = [[0 for i in range(dim)] for j in range(dim)]
    dirs = "lu,u,ru,l,r,ld,d,rd".split(",")
    offset = {}

    for dir in dirs:
        os = 0
        if "l" in dir:
            os -= 1
        if "r" in dir:
            os += 1
        if "u" in dir:
            os -= cols
        if "d" in dir:
            os += cols
        offset[dir] = os

    for longrow in range(dim):
        row,col = divmod(longrow,cols)
        upbad = row == 0
        downbad = row == rows - 1
        leftbad = col == 0
        rightbad = col == cols - 1
        for dir in dirs:
            row,col = divmod(longrow,cols)
            bad = (   ("l" in dir and leftbad)
                   or ("r" in dir and rightbad)
                   or ("u" in dir and upbad)
                   or ("d" in dir and downbad)
                  )
            if not bad:
                mat[longrow][longrow + offset[dir]] = 1
    return mat

def triplets(mat):
    rows = len(mat)
    cols = len(mat[0])
    for row in range(1,rows):
        assert len(mat[row]) == cols,"non-rectangular data"

    paths = []
    for row in range(rows):
        for midpoint in range(cols):
            if mat[row][midpoint]:
                for col in range(cols):
                    fin = mat[midpoint][col]
                    if fin and col != row:
                        paths.append((row,midpoint,col))
    return paths

def newseqs(mat,seq):
    rows = len(mat)
    cols = len(mat[0])
    for row in range(1,rows):
        assert len(mat[row]) == cols,"non-rectangular data"

    row = seq[-1]
    appendages = [index for index in range(cols) if mat[row][index] and index not in seq]
    return [seq + (index,) for index in appendages]

        
if __name__ == "__main__":

    mat = adjacency(4,5)
    """
    for row in mat:
        for item in range(len(row)):
            print row[item], 
            if not (item + 1) % 5:
                print
        print

    mat = adjacency(4,4)
    for row in mat:
        for item in range(len(row)):
            print row[item], 
            if not (item + 1) % 4:
                print
        print
    
    trips = triplets(mat)
    for trip in trips:
        print " ".join([str(item) for item in trip])

    """
    
    #print mat
    assert newseqs(mat,(5,6,7)) == [(5, 6, 7, 1), (5, 6, 7, 2),
                              (5, 6, 7, 3), (5, 6, 7, 8),
                              (5, 6, 7, 11), (5, 6, 7, 12),
                              (5, 6, 7, 13)]

    

