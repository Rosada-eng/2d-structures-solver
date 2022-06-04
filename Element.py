import numpy as np

class K:
    def __init__(self, element_number, node1, node2):
        self.element_number = element_number
        self.ids = [node1.x.id, node1.y.id, node2.x.id, node2.y.id]
        self.matrix = None

    def __str__(self):
        return f"Ke_{self.element_number}: \t {self.ids} \n\n {self.matrix}"


class Element:
    def __init__(self, element_number, node1, node2, section_area, elasticity):
        self.number = element_number
        self.n1 = node1
        self.n2 = node2
        self.components = f"{node1.number}-{node2.number}"
        self.A = section_area
        self.E = elasticity
        self.Ke = K(element_number, node1, node2)
        self.Ke.matrix = self.global_stiffness()

    def __str__(self):
        return "Elemento {0}: ({1}-{2}) {({4},{5}) ; ({6},{7})}".format(self.number, self.n1.number, self.n2.number, self.n1.x, self.n1.y, self.n2.x, self.n2.y)

    def length(self):
        return self.n1.distance_to(self.n2)

    def angle(self):
        return np.arctan2(self.n2.y - self.n1.y, self.n2.x - self.n1.x)

    def stiffness_module(self):
        return self.E * self.A / self.length()

    def global_stiffness(self):
        theta = self.angle()
        c = np.cos(theta)
        s = np.sin(theta)
        return self.stiffness_module() * np.array([
                [c**2, c*s, -c**2, -c*s],
                [c*s, s**2, -c*s, -s**2],
                [-c**2, -c*s, c**2, c*s],
                [-c*s, -s**2, c*s, s**2]])
