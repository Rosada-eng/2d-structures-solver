import sys, getopt
from src.Element import *
from src.Node import *
from src.Trellis import *
from utils.funcoesTermosol import geraSaida, importa, plota
from utils.utils import *

def main(argv):
    inputfile = ''
    outputfile = ''
    amplification = 1.0

    try:
        opts, args = getopt.getopt(argv, "hi:o:a:", ["input=", "output="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile> -a <amplification>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile> -a <amplification>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
        elif opt in ("-a", "--amplification"):
            amplification = float(arg)
        
    print("Input file is " + inputfile)
    print("Output file is " + outputfile)
        
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
    nn, N, nm, Inc, nc, F, nr, R = importa(inputfile)

    count_number = 1
    count_ids = 0

    # Constrói os nós
    nodes = {}
    for i in range(0, nn):
        new_node = Node(count_number, count_ids, N[0][i], count_ids+1, N[1][i])
        nodes[count_number] = new_node
        count_ids += 2
        count_number += 1

    count_number = 1

    # Constrói treliça
    trellis = Trellis(num_nodes=nn)
    elements = {}
    for i in range(0, nm):
        new_element = Element(count_number, nodes[Inc[i][0]], nodes[Inc[i][1]], Inc[i][3], Inc[i][2])
        elements[count_number] = new_element
        count_number += 1
        trellis.add_element(new_element)

    trellis.calc_Kg()

    # Matriz Kg reduzida com índices das reações conhecidas
    red_size = 2 * nn - nr # tamanho da matriz reduzida
    reduced_kg = np.zeros((red_size, red_size))
    i_kg = 0
    j_kg = 0
    for i in range(0, 2 * nn):
        for j in range(0, 2 * nn):
            if np.isin(R, [i, j]).sum() == 0:
                reduced_kg[i_kg][j_kg] = trellis.Kg.matrix[i, j]
                j_kg += 1
                if j_kg >= red_size:
                    j_kg = 0
                    i_kg += 1

    # Matriz F com índices das reações conhecidas
    reduced_F = np.zeros((2*nn - nr, 1))
    i_f = 0
    for i in range(0, 2 * nn):
        if np.isin(R, [i]).sum() == 0:
            reduced_F[i_f] = F[i, 0]
            i_f += 1

    # Deslocamento e erro máximo obtido
    """
        Para usar o método de Jacobi, basta trocar o método abaixo
    """
    disp_reduced, max_err = gauss_seidel(1e3, reduced_kg, reduced_F, 1e-6)
    disp_full = np.zeros((2*nn, 1))
    i_d = 0
    for i in range(0, 2 * nn):
        if np.isin(R, [i]).sum() == 0:
            disp_full[i] = disp_reduced[i_d]
            i_d += 1

    print("\nDeslocamentos [m]")
    print(disp_full)

    # Atribuição dos deslocamentos aos nós
    for i in range(0, nn - 1):
        trellis.elements[i].n1.dx = disp_full[2*i]
        trellis.elements[i].n1.dy = disp_full[2*i + 1]
        trellis.elements[i].n2.dx = disp_full[2*i + 2]
        trellis.elements[i].n2.dy = disp_full[2*i + 3]

    # Atribuição dos deslocamentos à treliça
    trellis.displacements = disp_full

    # Cálculo das reações desconhecidas
    reactions = np.zeros((nr, 1))
    i_r = 0
    for i in range(0, 2*nn):
        if np.isin(R, [i]).sum() > 0:
            reactions[i_r] = np.dot(trellis.Kg.matrix[i, :], disp_full)
            i_r += 1

    print("\nReações de apoio [N]")
    print(reactions)

    # Matriz de deformação
    trellis.calc_deforms()

    print("\nDeformações []")
    print(trellis.deforms)
    
    # Matriz de tensões
    trellis.calc_strains()

    print("\nTensões internas [Pa]")
    print(trellis.strains)

    A_vec = np.array([[e.A] for e in trellis.elements])
    internal_forces = trellis.strains * A_vec

    print("\nForças internas [N]")
    print(internal_forces)


    # filter disp_full by even indexes
    disp_full_X = disp_full[::2]
    disp_full_Y = disp_full[1::2]

    print("Desloc X \n", disp_full_X)
    print("Desloc Y \n", disp_full_Y)

    if inputfile == 'entrada.xls':
        print("Fator recomendado de amplificação: ", 1e4)
        # amplification = 1e4

    elif inputfile == 'entrada2.xls':
        print("Fator recomendado de amplificação: ", 0.04156014)
        # amplification =  0.04156014

    # else:
    #     amplification = 1
 

    deformed = [disp_full_X, disp_full_Y ]
    deformed = np.reshape(deformed, (2, nn))

    deformed = deformed * amplification
    deformed = N + deformed
    plota(N, Inc, deformed)

    # Gera o arquivo de saída
    geraSaida(outputfile, reactions, disp_full, trellis.deforms, internal_forces, trellis.strains)

if __name__ == '__main__':
    main(sys.argv[1:])