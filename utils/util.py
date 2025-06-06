import numpy as np
import json

def create_stochastic_matrix(num_states):
    mask = np.random.rand(num_states,num_states)
    mask_row_sum = mask.sum(axis=1)
    P = mask  / mask_row_sum[:,None]
    return P

def create_matrix_from_eig_value(num_states, eig_value):
    n = num_states
    w = []
    w.append(1)
    w.append(eig_value)
    w[2:n+1] = [np.random.uniform(0, w[1]) for i in range(2, n)]
    lamda = sorted(w, reverse = True)
    lamda = np.append(lamda, 0)
    A = np.zeros((n, n))
    alpha = np.zeros(n)
    for j in range(len(A[0])):
        alpha[j] = lamda[j] - lamda[j + 1]

    for j in range(n):
        for k in range(n):
            if k <= j:
                A[j, j] += alpha[k]/(n - k)        
            elif k > j:
                A[j, j] += alpha[k]

    mod_alpha = alpha / (n - np.arange(n))

    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = np.sum(mod_alpha[:(i + 1)])
            A[j, i] = A[i, j]
    return A

# Create a JSON Encoder class
class json_serialize(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
