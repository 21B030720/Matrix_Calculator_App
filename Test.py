import math


def vector_dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))


def vector_subtract(v1, v2):
    return [x - y for x, y in zip(v1, v2)]


def vector_multiply(v, scalar):
    return [x * scalar for x in v]


def vector_norm(v):
    return math.sqrt(vector_dot(v, v))


def vector_normalize(v):
    norm = vector_norm(v)
    return [x / norm for x in v]


def gram_schmidt(matrix):
    """ Apply Gram-Schmidt process to find orthonormal vectors (Q matrix). """
    n = len(matrix)
    m = len(matrix[0])
    Q = []

    for j in range(m):
        # Take the j-th column of the matrix
        v = [matrix[i][j] for i in range(n)]

        # Subtract the projections onto the previously computed q vectors
        for q in Q:
            projection = vector_multiply(q, vector_dot(q, v))
            v = vector_subtract(v, projection)

        # Normalize the vector to make it a unit vector
        q = vector_normalize(v)
        Q.append(q)

    # Return the matrix Q as column vectors
    return [[Q[i][j] for i in range(m)] for j in range(n)]


def multiply_matrices(A, B):
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            result[i][j] = sum(A[i][k] * B[k][j] for k in range(len(B)))
    return result


def qr_decomposition(A):
    Q = gram_schmidt(A)

    # Calculate R = Q^T * A
    Q_T = [[Q[j][i] for j in range(len(Q))] for i in range(len(Q[0]))]  # Transpose of Q
    R = multiply_matrices(Q_T, A)

    return Q, R
