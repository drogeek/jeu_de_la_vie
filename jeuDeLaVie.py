import numpy as np 
from itertools import product
from time import sleep

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cases = np.zeros([height,width],dtype=bool)
        self.neighbours_relative_indexes = list(product([-1,0,1],[-1,0,1]))
        self.neighbours_relative_indexes.remove((0,0))
    
    @staticmethod
    def from_np_array(array):
        w = World(*array.shape)
        w.cases = array
        return w

    def _getNeighboursNbr(self, cases, i, j):
        count = 0
        for ni in self.neighbours_relative_indexes:
            try:
                if cases[i+ni[0],j+ni[1]]:
                    count+=1 
            except IndexError:
                pass
        return count

    def __iter__(self):
        return self

    def __next__(self):
        backup_cases = self.cases.copy()
        for i, j in product(np.arange(self.width),np.arange(self.height)):
            neighboursNbr = self._getNeighboursNbr(backup_cases,i,j) 
            if self.cases[i,j]:
                if neighboursNbr < 2 or neighboursNbr > 3:
                    self.cases[i,j] = False
            else:
                if neighboursNbr == 3:
                    self.cases[i,j] = True
        #if np.all(np.logical_xor(backup_cases, self.cases) == np.zeros([self.width,self.height])):
        #    raise StopIteration
        return self

    def __str__(self):
        return self.cases.__str__()

if __name__ == "__main__":
    w = World(20,20)
    w.cases[5,5] = True
    w.cases[5,6] = True
    w.cases[5,7] = True
    w.cases[6,5] = True
    w.cases[7,5] = True
    w.cases[6,7] = True
    w.cases[7,7] = True
    for i in w: 
        print(w.cases.astype(int))
        sleep(0.3)
