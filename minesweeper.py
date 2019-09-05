import numpy as np
class Grid:
    a = None
    n = 0
    m = 0
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.a = np.zeros(n*n, dtype=int)
        coords = np.random.choice(np.arange(n*n), m)
        for coord in coords:
            self.a[coord] = -1 # mine
        self.a = self.a.reshape(n,n)
        for i in range(n):
            for j in range(n):
                if self.a[i][j] != -1:
                    self.a[i][j] = self.count_bombs(i, j)

    def count_bombs(self, i, j):
        increments = [(i-1,j-1), (i, j-1), (i+1, j-1),
                      (i-1,j),   (i, j),   (i+1, j),
                      (i-1,j+1), (i, j+1), (i+1, j+1)]
        f = lambda p : p[0] >= 0 and p[1] >= 0 and p[0] < self.n and p[1] < self.n
        increments = list(filter(f, increments))
        indices = np.array(list(map(lambda p : self.n*p[0] + p[1], increments)))
        bombs = np.array(list(map(lambda x : 1 if x == -1 else 0, self.a.flatten())))
        return np.sum(bombs[indices])

    def print(self):
        print('')
        print(self.a)

class Display:
    n = 0
    n = 0
    hidden = []
    flagged = []
    flagchar = '!'
    hiddenchar = '_'
    emptychar = ' '
    bombchar = '*'

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.hidden = np.zeros((n,n)) == 0
        self.flagged = np.zeros((n,n)) != 0

    def display(self, grid):
        for i in range(n):
            for j in range(n):
                if self.flagged[i][j]:
                    print(self.flagchar, end=' ')
                elif self.hidden[i][j]:
                    print(self.hiddenchar, end=' ')
                elif grid.a[i][j] == -1:
                    print(self.bombchar, end=' ')
                elif grid.a[i][j] == 0:
                    print(self.emptychar, end=' ')
                else:
                    print(grid.a[i][j], end=' ')
            print('')

    def display_all(self, grid):
        for i in range(n):
            for j in range(n):
                if self.flagged[i][j]:
                    print(self.flagchar, end=' ')
                elif grid.a[i][j] == -1:
                    print(self.bombchar, end=' ')
                elif grid.a[i][j] == 0:
                    print(self.emptychar, end=' ')
                else:
                    print(grid.a[i][j], end=' ')
            print('')

    def __get_neighbors(self, grid, i, j):
        increments = [(i-1,j-1), (i, j-1), (i+1, j-1),
                      (i-1,j), (i+1, j), (i-1,j+1), (i, j+1),
                      (i+1, j+1)]
        
        neighbors = []

        for inc in increments:
            if (inc[0] < 0) or (inc[1] < 0) or\
               (inc[0] >= grid.n) or (inc[1] >= grid.n):
               continue
            
            neighbors.append(inc)

        return neighbors

    def __expand_neighbors(self, grid, i, j):
        neighbors = self.__get_neighbors(grid, i, j)

        for n in neighbors:
            i_, j_ = n

            if (0 == grid.a[i_][j_]):
                if self.hidden[i_][j_]:
                    self.hidden[i_][j_] = False
                    self.__expand_neighbors(grid, i_, j_)
            else:
                self.hidden[i_][j_] = False
    
    def show(self, grid, i, j):
        self.hidden[i][j] = False
        if grid.a[i][j] == -1:
            return True
        
        self.__expand_neighbors(grid, i, j)

        return False
        
    def flag(self, grid, i, j):
        self.flagged[i][j] = True
        if grid.a[i][j] == -1:
            return True
        self.m -= 1
        return False

n = 9
m = 4
lose = False
grid = Grid(9,4)
grid.print()
d = Display(n, m)
d.display(grid)

while not lose:
    t = input('s/f: ')
    i = int(input('i: '))
    j = int(input('j: '))
    if t == "s":
        lose = d.show(grid, i, j)
    elif t == 'f':
        d.flag(grid, i, j)
    else:
        print('Invalid move')
    d.display(grid)

print('You lost!')
d.display_all(grid)
