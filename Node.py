class Coord:
    def __init__(self, _id, value):
        self.id = _id           # id utilizado para identificar a componente na matriz K
        self.value = value

class Node(Coord):
    def __init__(self, number, idx, x, idy, y):
        self.number = number
        self.x = Coord(idx, x)
        self.y = Coord(idy, y)

    def __str__(self) -> str:
        return f"Nó {self.number}: (x, y) = ({self.x.value}, {self.y.value}) | (idx, idy) = ({self.x.id}, {self.y.id})"

    def distance_to(self, node):
        return ((self.x.value - node.x.value)**2 + (self.y.value - node.y.value)**2)**0.5

    #TODO: Adicionar métodos convenientes para cálculo
