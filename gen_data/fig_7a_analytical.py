'''
Module Description

Classes:
    None
'''

import numpy as np
import pandas as pd
import json

import random

from utils.util import create_matrix_from_eig_value
from utils.util import json_serialize

SEED = 123
random.seed(SEED)
np.random.seed(SEED)
np.random.default_rng(SEED)

SECOND_EIG_VALUE_OF_TPM = 0.85

S = 6
A = 3

P = create_matrix_from_eig_value(S, SECOND_EIG_VALUE_OF_TPM) 
print(P)
eig_val, eig_vec = np.linalg.eig(P.T)
STATIONARY_STATE_DIST = np.array(eig_vec[:, np.where(np.abs(eig_val - 1.) < 1e-8)[0][0]].flat)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST / np.sum(STATIONARY_STATE_DIST)
STATIONARY_STATE_DIST = STATIONARY_STATE_DIST.real
print(STATIONARY_STATE_DIST)
#P = np.array([P])
#STATIONARY_STATE_DIST = np.array([STATIONARY_STATE_DIST])

R = np.array([
    [50, 0, 0],
    [0, 0, 50],
    [0, 50, 0],
    [0, 50, 0],
    [0, 0, 50],
    [50, 0, 0]])

if R.shape[0] != S or R.shape[1] != A:
    raise ValueError("R shape should be SxA")

MU_DD = np.array([0.55])
LAMBDA_DD = np.array([0.4])
MU_UU = np.array([0.3,0.45])
LAMBDA_UU = np.round(np.arange(0.05,1,0.05), 2)
pmf_of_aoi={}

def compute_pmf_of_aoi(lambda_, mu_, delta_):
    if lambda_ not in pmf_of_aoi:
        pmf_of_aoi[lambda_] = {}
    if mu_ not in pmf_of_aoi[lambda_]:
        pmf_of_aoi[lambda_][mu_] = {}
    if delta_ not in pmf_of_aoi[lambda_][mu_]:
        term_1 = ((mu_ - lambda_)*(((1 - mu_)/(1 - lambda_))**(delta_ + 1)))/(1 - mu_)
        term_2 = (((1 - lambda_)**(delta_ + 1)) * lambda_ * mu_)/(mu_ - lambda_)
        term_3 = lambda_ * mu_ * ((1 - mu_)**delta_)*(2 + delta_)
        term_4 = (((1 - mu_)**(delta_))*(((1 + mu_) * (lambda_**2))-(lambda_ * mu_ * (1 + 2 * mu_))+(mu_ ** 2)))/(lambda_ - mu_)    
        pmf_of_aoi[lambda_][mu_][delta_] = (term_1 + term_2 - term_3 + term_4)
    return pmf_of_aoi[lambda_][mu_][delta_]

lambda_dd = LAMBDA_DD
#lambda_dd=[0.001,0.05,1.0]## TEST
lambda_uu = LAMBDA_UU
mu_dd = MU_DD
mu_uu = MU_UU

#no_of_steps = NO_OF_STEPS
no_of_steps = 100000

astar = np.argmax(R, axis=1)
print(astar)

dict_rewards = {}
dict_rewards["mu_d"] = {"lambda_d":{"mu_u":"lambda_u"}}
dict_rewards["rewards"] = {}
for mu_d in mu_dd:
    if mu_d == 1.0:
        break
    print("mu_d = "+str(mu_d))
    dict_rewards["rewards"][mu_d] = {}
    for lambda_d in lambda_dd:
        if lambda_d >= mu_d and mu_d != 1.0:
            break
        print("lambda_d = "+str(lambda_d))
        dict_rewards["rewards"][mu_d][lambda_d] = {}
        for mu_u in mu_uu:
            if mu_u == 1.0:
                break
            print("mu_u = "+str(mu_u))
            dict_rewards["rewards"][mu_d][lambda_d][mu_u] = {}   
            for lambda_u in lambda_uu:
                if lambda_u >= mu_u and mu_u != 1.0:
                    break
                print("lambda_u = "+str(lambda_u))
                avg_reward = 0
                #P_temp = np.eye(6)
                #P_temp = P                
                for delta_u in range(no_of_steps):
                    lambda_u_temp = compute_pmf_of_aoi(lambda_u, mu_u, delta_u)
                    if lambda_u_temp <= 1e-8:
                        break
                    #P_temp1 = P_temp
                    #P_temp1 = np.eye(6)                    
                    for delta_d in range(no_of_steps):
                        lambda_d_temp = compute_pmf_of_aoi(lambda_d, mu_d, delta_d)
                        if lambda_d_temp*lambda_u_temp <= 1e-8:
                            break
                        P_temp1 = np.linalg.matrix_power(P, delta_u + delta_d)
                        P_temp = np.linalg.matrix_power(P, delta_u)
                        s_ML = np.argmax(P_temp, axis=-1)
                        temp = 0
                        for index,state in enumerate(s_ML):
                            #temp += (STATIONARY_STATE_DIST@P_temp[:,state])*(P_temp1[index,:]@R.T[astar[state],:])
                            ## here (STATIONARY_STATE_DIST@P_temp[:,state]) = STATIONARY_STATE_DIST[index] may not be true for a general stochastic matrix
                            temp += STATIONARY_STATE_DIST[index]*(P_temp1[index,:]@R.T[astar[state],:])
                        avg_reward += lambda_d_temp*lambda_u_temp*temp 
                        #P_temp1 = P_temp1@P
                    #P_temp = P_temp@P
                dict_rewards["rewards"][mu_d][lambda_d][mu_u][lambda_u] = avg_reward

print(pd.DataFrame(dict_rewards["rewards"]))

#file_name=SIM_NAME+"_data3.json"    
file_name="sim/sim3_data3_085.json"    
with open(file_name, 'w') as file:
    json.dump(dict_rewards, file, ensure_ascii=False, cls=json_serialize)
