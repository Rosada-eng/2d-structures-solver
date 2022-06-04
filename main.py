from Element import *
from funcoesTermosol import geraSaida, importa, plota
from Node import *
from Trellis import *

if __name__ == '__main__':
    """
    nn = numero de nos
    N = matriz dos nos
    nm = numero de membros
    Inc = matriz de incidencia
    nc = numero de cargas
    F = vetor carregamento
    nr = numero de restricoes
    R = vetor de restrições
    """
    nn, N, nm, Inc, nc, F, nr, R = importa("entrada.xls")

    count_number = 1
    count_ids = 0

    print(f"----- Building {nn} Nodes: ----- \n")
    # Constrói os nós
    nodes = {}
    for i in range(0, nn):
        new_node = Node(count_number, count_ids, N[0][i], count_ids+1, N[1][i])
        print(new_node)
        nodes[count_number] = new_node
        count_ids += 2
        count_number += 1

    count_number = 1

    print(f"----- Building {nm} Elements: ----- \n")
    # Constrói treliça
    trellis = Trellis()
    elements = {}
    for i in range(0, nm):
        new_element = Element(count_number, nodes[Inc[i][0]], nodes[Inc[i][1]], Inc[i][3], Inc[i][2])
        print(new_element.Ke)
        elements[count_number] = new_element
        count_number += 1
        trellis.add_element(new_element)

    trellis.calc_Kg()

    # print([element.Ke.ids for element in trellis.elements])
    print(trellis.Kg.matrix)

    # print(F, nc)
    # print(R, nr)
    
