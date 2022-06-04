import numpy as np

from Element import Element


class Kg:
    def __init__(self, n_nos):
        self.ids = range(1, n_nos+1)                      # Guarda uma lista com o id de cada coordenada da Treliça
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
            if np.isin(element.Ke.ids, indexes_list).sum() >= 2: # + de 2 Trues no array comparado
                elements.append(element)

        return elements

    def calc_Kg(self):
        self.Kg = Kg(len(self.elements))

        for i in range(1, 2*len(self.elements)+1):
            for j in range(1, 2*len(self.elements)+1):

                # Selecionar os elementos que contém o id i e j
                elements = self._find_elements_with_indexes_in_K([i, j])
                for element in elements:
                    _i = element.Ke.ids.index(i) - 1
                    _j = element.Ke.ids.index(j) - 1
                    self.Kg.matrix[i - 1][j - 1] += element.Ke.matrix[_i][_j]

# k1 = [0,1,2,3]
# k2 = [0,1,4,5]
# k3 = [2,3,4,5]

# print(np.isin(k3, [2,3]).sum())
