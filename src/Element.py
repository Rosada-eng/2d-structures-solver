import numpy as np

from .Node import Node


class K:
    def __init__(self, element_number, node1, node2):
        self.element_number = element_number
        self.ids = [node1.x.id, node1.y.id, node2.x.id, node2.y.id]
        self.matrix = None

    def __str__(self):
        return f"Ke_{self.element_number}: \t {self.ids} \n\n {self.matrix}"


class Element:
    def __init__(self, element_number, node1: Node, node2: Node, section_area, elasticity):
        self.number = element_number
        self.n1 = node1
        self.n2 = node2
        self.components = f"{node1.number}-{node2.number}"
        self.A = section_area
        self.E = elasticity
        self.Ke = K(element_number, node1, node2)
        self.Ke.matrix = self.global_stiffness()

    def __str__(self):
        return f"Elemento {self.number}: Nós({self.n1.number}-{self.n2.number}) | ids({self.Ke.ids}) | A= {self.A} E= {self.E}"

    def length(self):
        """
        Calcula o comprimento da barra
        """
        return self.n1.distance_to(self.n2)

    def stiffness_module(self):
        """
        Calcula o módulo de rigidez da barra
        """
        return self.E * self.A / self.length()

    def global_stiffness(self):
        """
        Calcula a matriz de rigidez global
        """
        s = (self.n2.y.value - self.n1.y.value) / self.length()
        c = (self.n2.x.value - self.n1.x.value) / self.length()
        return self.stiffness_module() * np.array([
                [c**2, c*s, -c**2, -c*s],
                [c*s, s**2, -c*s, -s**2],
                [-c**2, -c*s, c**2, c*s],
                [-c*s, -s**2, c*s, s**2]])

    def deform(self):
        """
        Calcula a deformação da barra
        """
        s = (self.n2.y.value - self.n1.y.value) / self.length()
        c = (self.n2.x.value - self.n1.x.value) / self.length()
        t_array = np.array([-c, -s, c, s])
        dxy = np.array([self.n1.dx, self.n1.dy, self.n2.dx, self.n2.dy])
        return (1/self.length()) * np.dot(t_array, dxy)

    def strain(self):
        """
        Calcula a tensão da barra
        """
        s = (self.n2.y.value - self.n1.y.value) / self.length()
        c = (self.n2.x.value - self.n1.x.value) / self.length()
        t_array = np.array([-c, -s, c, s])
        dxy = np.array([self.n1.dx, self.n1.dy, self.n2.dx, self.n2.dy])
        return (self.E / self.length()) * np.dot(t_array, dxy)

