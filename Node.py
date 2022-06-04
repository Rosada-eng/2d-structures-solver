class Coord:
    def __init__(self, _id, value):
        self.id = _id           # id utilizado para identificar a componente na matriz K
        self.value = value

class Node(Coord):
    def __init__(self, number, idx, x, idy, y):
        self.number = number
        self.x = Coord(idx, x)
        self.y = Coord(idy, y)

    def distance_to(self, node):
        return ((self.x - node.x.value)**2 + (self.y - node.y.value)**2)**0.5

    #TODO: Adicionar métodos convenientes para cálculo
