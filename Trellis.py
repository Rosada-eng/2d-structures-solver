import numpy as np

from Element import Element


class Kg:
    def __init__(self, n_nos):
        self.ids = range(0, n_nos)                      # Guarda uma lista com o id de cada coordenada da Treliça
        self.matrix = np.zeros((2*n_nos, 2*n_nos))


class Trellis(Kg):
    def __init__(self, elements=[]):
        self.elements = elements
        self.Kg = None

    def add_element(self, element: Element):
        self.elements.append(element)

    def _find_elements_with_indexes_in_K(self, indexes_list):
        """ 
            Retorna uma lista de elementos cujo Ke é composto pelos id's que procuramos
        """
        elements = []
        for element in self.elements:
            # Se os dois ids compõem o elemento, adiciona o elemento à lista
            if( indexes_list[0] in element.Ke.ids) and (indexes_list[1] in element.Ke.ids):
                elements.append(element)

        # print(f"{len(elements)} elementos com os id's {indexes_list}: {[element.number for element in elements]}")
        return elements

    def calc_Kg(self):
        self.Kg = Kg(len(self.elements))

        for i in range(0, 2*len(self.elements)):
            for j in range(0, 2*len(self.elements)):

                # Selecionar os elementos que contém o id i e j
                elements = self._find_elements_with_indexes_in_K([i, j])
                for element in elements:
                    _i = element.Ke.ids.index(i) 
                    _j = element.Ke.ids.index(j)
                    self.Kg.matrix[i][j] += element.Ke.matrix[_i][_j]
