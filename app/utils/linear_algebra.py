import numpy as np

RELATIVE_PIVOT_TOLERANCE = 1e-12


def determinant(matrix: np.ndarray) -> float:
    work = np.array(matrix, dtype=float)
    size = work.shape[0]
    scale = max(1.0, float(np.max(np.abs(work))))
    threshold = RELATIVE_PIVOT_TOLERANCE * scale
    sign = 1.0
    for k in range(size):
        pivot_row = k + int(np.argmax(np.abs(work[k:, k])))
        if abs(work[pivot_row, k]) < threshold:
            return 0.0
        if pivot_row != k:
            work[[k, pivot_row]] = work[[pivot_row, k]]
            sign = -sign
        for i in range(k + 1, size):
            factor = work[i, k] / work[k, k]
            work[i, k:] = work[i, k:] - factor * work[k, k:]
    result = sign
    for k in range(size):
        result *= work[k, k]
    return float(result)


def replace_column(matrix: np.ndarray, index: int, vector: np.ndarray) -> np.ndarray:
    modified = np.array(matrix, dtype=float)
    modified[:, index] = vector
    return modified
