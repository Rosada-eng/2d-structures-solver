import numpy as np


def jacobi(ite, reduced_K, reduced_F, tol=1e-7):
    """
    Jacobi's iteration method
    """
    u = np.zeros((reduced_F.shape[0], 1))
    u_old = np.zeros((reduced_F.shape[0], 1))
    _tol = np.ones((reduced_F.shape[0], 1))

    count = 0

    # Inicialização
    while (count < ite) and ((_tol > tol).sum() != 0):
        # Registra deslocamento antigo
        u_old = np.copy(u)
        for u_i in range(0, u.shape[0]):

            # K e u sem o elemento de índice u_i
            K_temp = np.delete(reduced_K[u_i,:], u_i)
            u_temp = np.delete(u_old, u_i)

            u[u_i] = (reduced_F[u_i] - np.dot(K_temp, u_temp)) / reduced_K[u_i][u_i]
            
            # Calcula erro
            if u[u_i] != 0:
                _tol[u_i,0] = abs((u[u_i,0] - u_old[u_i,0]) / u[u_i,0])

        count += 1

    return u, np.max(_tol)

def gauss_seidel(ite, reduced_K, reduced_F, tol=1e-7):
    """
    Gauss-Seidel's iteration method
    """
    u = np.zeros((reduced_F.shape[0], 1))
    u_old = np.zeros((reduced_F.shape[0], 1))
    _tol = np.ones((reduced_F.shape[0], 1))

    count = 0

    # Inicialização
    while (count < ite) and ((_tol > tol).sum() != 0):
        for u_i in range(0, u.shape[0]):

            # K e u sem o elemento de índice u_i
            K_temp = np.delete(reduced_K[u_i,:], u_i)
            u_temp = np.delete(u_old, u_i)

            u[u_i] = (reduced_F[u_i] - np.dot(K_temp, u_temp)) / reduced_K[u_i][u_i]

            # Calcula erro
            if u[u_i] != 0:
                _tol[u_i,0] = abs((u[u_i,0] - u_old[u_i,0]) / u[u_i,0])

            # Atualiza deslocamento do elemento para o próximo passo
            u_old[u_i] = u[u_i]

        count += 1

    return u, np.max(_tol)
